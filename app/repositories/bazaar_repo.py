

from datetime import datetime, timedelta, timezone
import logging

from sqlalchemy import case, func, select

from app.core.utils.normalize_product_id import normalize_product_id
from app.repositories.base import Baserepository
from app.models.price import BazaarPrice


log = logging.getLogger(__name__)

class BazaarRepository(Baserepository):
    async def save_prices(self, prices: list[dict]) -> int:
        if not prices:
            return 0
        objects = [BazaarPrice(**p) for p in prices]
        try:
            self.session.add_all(objects)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            log.exception("Ошибка сохранения bazaar в БД")
            raise
        return len(objects)
        

    async def get_history(self, product_id: str, limit: int = 100):
        pid = normalize_product_id(product_id)
        stmt = (
            select(BazaarPrice)
            .where(BazaarPrice.product_id == pid)
            .order_by(BazaarPrice.timestamp.desc())
            .limit(limit)
        )
        # result с await является действием и хранится 1 раз 
        result = await self.session.execute(stmt)
        data = result.scalars().all()
        
        dict_data = []
        for item in data:
            
            dict_data.append({
            "product_id": item.product_id,
            "buy_price": item.buy_price,
            "sell_price": item.sell_price,
            "buy_volume": item.buy_volume,
            "sell_volume": item.sell_volume,
            'buy_moving_week': item.buy_moving_week,
            'sell_moving_week': item.sell_moving_week,
            'buy_orders': item.buy_orders,
            'sell_orders': item.sell_orders,
            "timestamp": item.timestamp
        })
        
        return dict_data 
        
        
    async def search_products(self, search: str, limit: int = 20,) -> list[dict]:
        """Поиск bazaar-продуктов по подстроке в product_id.

        Пустой `search` → топ активных (по алфавиту).
        """
        since = datetime.now(timezone.utc) - timedelta(days=30)
        s = normalize_product_id(search)
        stmt = (
            select(
                BazaarPrice.product_id,
                func.max(BazaarPrice.timestamp).label("last_seen"),
            )
            .where(BazaarPrice.timestamp >= since)
            .group_by(BazaarPrice.product_id)
        )

        if s:
            col = BazaarPrice.product_id
            stmt = stmt.where(col.contains(s, autoescape=True))
            rank = case(
                (col == s, 0),
                (col.startswith(s, autoescape=True), 1),
                else_=2,
            )
            
            stmt = stmt.order_by(rank, BazaarPrice.product_id)
        else:
            stmt = stmt.order_by(BazaarPrice.product_id)

        stmt = stmt.limit(limit)
        rows = (await self.session.execute(stmt)).all()

        result = []
        for pid, last_seen in rows:
            result.append({
                "product_id": pid,
                "last_seen": last_seen,
            })
        return result