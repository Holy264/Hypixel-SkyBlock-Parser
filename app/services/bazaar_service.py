import logging
from app.core.hypixel_client import HypixelClient
from app.repositories.bazaar_repo import BazaarRepository

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

            to_save.append({
                "product_id": product_id,
                "buy_price": quick["buyPrice"],
                "sell_price": quick["sellPrice"],
                "buy_volume": quick["buyVolume"],
                "sell_volume": quick["sellVolume"],
                'buy_moving_week': quick["buyMovingWeek"],
                'sell_moving_week': quick["sellMovingWeek"],
                'buy_orders': quick["buyOrders"],
                'sell_orders': quick["sellOrders"],
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