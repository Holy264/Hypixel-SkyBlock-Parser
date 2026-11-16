import asyncio
from core.config import settings
from core.hypixel_client import HypixelClient
from models.product_categories import PRODUCT_TO_CATEGORY

async def main():
    client = HypixelClient(api_key=settings.hypixel_api_key)
    try:
        data = await client.get_bazaar()
    finally:
        await client.close()

    api_ids = set(data["products"].keys())
    map_ids = set(PRODUCT_TO_CATEGORY.keys())
    unknown = sorted(api_ids - map_ids)

    print(f"В API: {len(api_ids)}, в маппинге: {len(map_ids)}")
    if unknown:
        print(f"\n❌ НЕ НАЙДЕНО ({len(unknown)}):")
        for pid in unknown:
            print(f"   {pid}")
    else:
        print("\n✅ Полное совпадение!")

asyncio.run(main())