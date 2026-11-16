"""
Запрашивает Bazaar, сравнивает с маппингом, показывает что не резолвится.
python -m scripts.audit_unknown
"""
import asyncio
from collections import defaultdict

from core.config import settings
from core.hypixel_client import HypixelClient
from models.product_categories import (PRODUCT_TO_CATEGORY, MANUAL_CATEGORIES, classify_by_pattern,)


async def main():
    client = HypixelClient(api_key=settings.hypixel_api_key)
    try:
        data = await client.get_bazaar()
    finally:
        await client.close()

    api_ids = list(data["products"].keys())
    by_source = defaultdict(list)
    unresolved = []

    for pid in api_ids:
        if pid in PRODUCT_TO_CATEGORY:
            by_source["slugify/overrides"].append(pid)
        elif pid in MANUAL_CATEGORIES:
            by_source["manual"].append(pid)
        elif classify_by_pattern(pid):
            by_source["prefix"].append(pid)
        else:
            unresolved.append(pid)

    print(f"Всего в API: {len(api_ids)}")
    for src, ids in by_source.items():
        print(f"  {src:20s} {len(ids)}")
    print(f"  {'UNRESOLVED':20s} {len(unresolved)}")

    if unresolved:
        print("\n❌ Не резолвится (добавьте в MANUAL_CATEGORIES):")
        for pid in sorted(unresolved):
            print(f"   {pid}")


asyncio.run(main())