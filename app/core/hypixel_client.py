import asyncio
import base64
import gzip
import io
import logging
import re

import httpx
import nbtlib

BASE_URL = "https://api.hypixel.net/v2"

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# Rarity из NBT (для /auctions_ended, где нет поля tier)
# ═══════════════════════════════════════════════════════════════════
_RARITY_BY_COLOR: dict[str, str] = {
    "§f": "COMMON",
    "§a": "UNCOMMON",
    "§9": "RARE",
    "§5": "EPIC",
    "§6": "LEGENDARY",
    "§d": "MYTHIC",
    "§b": "DIVINE",
    "§c": "SPECIAL",
    "§4": "VERY SPECIAL",
    "§e": "ULTIMATE",   
}

# Отрезаем префиксы вида "[§7Lvl 100§8] " или "[Lvl 100] "
_BRACKET_PREFIX_RE = re.compile(
    r"^(?:§[0-9a-fk-or])*\[[^\]]*\]\s*",
    flags=re.IGNORECASE,
)


def _tier_from_colored_name(name: str) -> str | None:
    """Извлекает редкость из строки с §-кодами.

    Формат Hypixel: '[§7Lvl 100§8] §5Enderman' → §5 → EPIC
    Обычные предметы: '§6Hyperion' → §6 → LEGENDARY
    """
    if not name:
        return None
    clean = _BRACKET_PREFIX_RE.sub("", name)
    # Первый §-код после префикса — цвет редкости
    for i in range(len(clean) - 1):
        if clean[i] == "§":
            rarity = _RARITY_BY_COLOR.get(clean[i:i + 2].lower())
            if rarity:
                return rarity
    return None

# ═══════════════════════════════════════════════════════════════════
# NBT helpers
# ═══════════════════════════════════════════════════════════════════
def _decode_nbt(item_bytes: str):
    """base64(gzip(NBT)) → nbtlib.File или None при ошибке."""
    if not item_bytes or nbtlib is None:
        return None
    try:
        raw = base64.b64decode(item_bytes)
        decompressed = gzip.decompress(raw)
        return nbtlib.File.parse(io.BytesIO(decompressed))
    except Exception as e:
        logger.warning("[auction] NBT decode fail: %s", e)
        return None


def _walk_nbt(node, key: str, depth: int = 0, max_depth: int = 8):
    """Рекурсивно ищет ключ `key` внутри любого Compound/List."""
    if node is None or depth > max_depth:
        return None

    try:
        if key in node:
            return node[key]
    except TypeError:
        pass

    if hasattr(node, "items"):
        try:
            for _k, v in node.items():
                found = _walk_nbt(v, key, depth + 1, max_depth)
                if found is not None:
                    return found
        except Exception:
            pass

    if isinstance(node, (list, tuple)) or (
        hasattr(node, "__iter__") and not isinstance(node, (str, bytes))
    ):
        try:
            for child in node:
                found = _walk_nbt(child, key, depth + 1, max_depth)
                if found is not None:
                    return found
        except Exception:
            pass

    return None


def extract_item_meta(item_bytes: str,) -> tuple[str | None, str | None] | None:
    """Возвращает (display_name, tier) из base64(gzip(NBT)).

    display_name — строка с §-кодами, как её отдаёт Hypixel;
    нормализуется позже через normalize_item_name().
    tier — редкость по цвету display.Name.

    None — если NBT не распарсился (отличать от «имени нет»).
    """
    nbt = _decode_nbt(item_bytes)
    if nbt is None:
        return None

    display = _walk_nbt(nbt, "display")
    if display is None or "Name" not in display:
        logger.debug("[auction] display.Name не найден в NBT")
        return None

    raw_name = str(display["Name"])
    if not raw_name:
        return None

    return raw_name, _tier_from_colored_name(raw_name)

# ═══════════════════════════════════════════════════════════════════
# HTTP-клиент
# ═══════════════════════════════════════════════════════════════════
class HypixelClient:
    def __init__(self, api_key: str = ""):
        headers: dict[str, str] = {}
        if api_key:
            headers["API-Key"] = api_key

        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=headers,
            timeout=30.0,
        )
    async def close(self) -> None:
            await self._client.aclose()
    # ───────────────────────────────────────────────────────────
    # Общий GET с retry / backoff
    # ───────────────────────────────────────────────────────────
    async def _get_with_retry(
        self,
        path: str,
        *,
        params: dict | None = None,
        max_retries: int = 3,
    ) -> dict:
        """GET с retry/backoff.

        Стратегия:
          - 4xx кроме 429  → raise сразу ;
          - 429            → backoff 15s, 30s, …
          - 5xx            → backoff 15s, 30s, …
          - сетевая ошибка → backoff 1s, 2s, 4s, …
        """
        last_exc: Exception | None = None

        for attempt in range(max_retries):
            is_last = attempt == max_retries - 1
            try:
                resp = await self._client.get(path, params=params)
                resp.raise_for_status()
                return resp.json()

            except httpx.HTTPStatusError as e:
                last_exc = e
                code = e.response.status_code

                if code != 429 and 400 <= code < 500:
                    raise

                if is_last:
                    break
                await asyncio.sleep(15 * (attempt + 1))

            except httpx.HTTPError as e:
                last_exc = e
                if is_last:
                    break
                await asyncio.sleep(2 ** attempt)

        raise last_exc or RuntimeError(
            f"{path}: исчерпаны попытки повторного выполнения "
            f"(params={params}, max_retries={max_retries})"
        )

    async def get_bazaar(self, max_retries: int = 3) -> dict:
        return await self._get_with_retry(
            "/skyblock/bazaar", max_retries=max_retries,
        )
    async def get_auctions(self, page: int = 0, max_retries: int = 3) -> dict:
        return await self._get_with_retry(
            "/skyblock/auctions",
            params={"page": page},
            max_retries=max_retries,
        )

    async def get_auctions_ended(self, max_retries: int = 3) -> dict:
        """Список недавно завершившихся аукционов (факты продаж)."""
        return await self._get_with_retry(
            "/skyblock/auctions_ended", max_retries=max_retries,
        )