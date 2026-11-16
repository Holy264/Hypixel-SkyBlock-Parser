import asyncio
import base64
import gzip
import io

import httpx
import nbtlib

from core.hypixel_client import extract_item_meta


def walk(node, prefix="", depth=0, max_depth=10):
    if depth > max_depth:
        return
    if hasattr(node, "items"):
        for k, v in node.items():
            if not hasattr(v, "items") and not isinstance(v, (list, tuple)):
                print(f"{prefix}{k} = {v!r}")
            else:
                print(f"{prefix}{k} →")
                walk(v, prefix + "  ", depth + 1)
    elif isinstance(node, (list, tuple)):
        for i, child in enumerate(node):
            print(f"{prefix}[{i}]")
            walk(child, prefix + "  ", depth + 1)


async def main():
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get("https://api.hypixel.net/v2/skyblock/auctions_ended")
        data = r.json()

    sales = data.get("auctions", [])
    print(f"Продаж: {len(sales)}")
    if not sales:
        return

    # один лот подробно
    ib = sales[0]["item_bytes"]
    print(f"item_bytes[:40] = {ib[:40]}")

    raw = base64.b64decode(ib)
    print(f"после base64 длина = {len(raw)} байт, первые 2 = {raw[:2].hex()}")

    decompressed = gzip.decompress(raw)
    print(f"после gzip длина = {len(decompressed)} байт")

    nbt = nbtlib.File.parse(io.BytesIO(decompressed))
    print(f"верхние ключи NBT: {list(nbt.keys())}")

    print("--- дерево NBT ---")
    walk(nbt)

    # проверка extract_item_id на всей пачке
    print("\n--- проверка extract_item_id ---")
    ok, fail = 0, 0
    examples_fail = []

    for s in sales:
        name = extract_item_meta(s.get("item_bytes", ""))
        if name:
            ok += 1
            if ok <= 5:
                print(f"  ✓ {name}")
        else:
            fail += 1
            if len(examples_fail) < 3:
                examples_fail.append((s.get("item_bytes") or "")[:60])

    print(f"\nУспешно: {ok}, провалилось: {fail}")
    for ex in examples_fail:
        print(f"  ✗ {ex}...")


asyncio.run(main())