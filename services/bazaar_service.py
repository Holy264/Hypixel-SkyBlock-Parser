import logging
from core.category_cache import FALLBACK_KEY, SUB_CATEGORY_CACHE, get_or_fallback
from core.hypixel_client import HypixelClient
from models.product_categories import resolve_category
from repositories.bazaar_repo import BazaarRepository

logger = logging.getLogger(__name__)


class BazaarService:
    def __init__(self, client: HypixelClient, repo: BazaarRepository):
        self.client = client
        self.repo = repo
        
        
    async def fetch_and_save(self) -> int:
        
        data = await self.client.get_bazaar()
        products = data.get("products", {})

        to_save: list[dict] = []
        uncategorized: list[str] = []

        for product_id, info in products.items():
            quick = info["quick_status"]
            
            cat = resolve_category(product_id)
            sub_id = get_or_fallback(cat)

            if sub_id is None:
                # Даже fallback нет — БД ещё не засеяна
                uncategorized.append(product_id)
                continue
            
            fallback_id = SUB_CATEGORY_CACHE.get(FALLBACK_KEY)
            if sub_id == fallback_id and cat is None:
                uncategorized.append(product_id)

            to_save.append({
                "product_id": product_id,
                "sub_category_id": sub_id,
                "buy_price": quick["buyPrice"],
                "sell_price": quick["sellPrice"],
                "buy_volume": quick["buyVolume"],
                "sell_volume": quick["sellVolume"],
            })

        if uncategorized:
            sample = ", ".join(uncategorized[:10])
            logger.warning(
                "[bazaar] %d без категории (fallback в Unknown):\n%s",
                len(uncategorized), sample,
            )

        if to_save:
            await self.repo.save_prices(to_save)
        return len(to_save)