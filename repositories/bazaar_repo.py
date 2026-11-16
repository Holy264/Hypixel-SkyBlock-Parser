

from datetime import datetime, timedelta, timezone
import logging

from sqlalchemy import case, func, select

from core.utils.normalize_product_id import normalize_product_id
from models.category import MainCategory, SubCategory
from models.product_categories import PRODUCT_ID_TO_DISPLAY, resolve_category
from repositories.base import Baserepository
from models.price import BazaarPrice


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
            select(BazaarPrice, MainCategory.name, SubCategory.name)
            .join(SubCategory, BazaarPrice.sub_category_id == SubCategory.id)
            .join(MainCategory, SubCategory.main_category_id == MainCategory.id)
            .where(BazaarPrice.product_id == pid)
            .order_by(BazaarPrice.timestamp.desc())
            .limit(limit)
        )
        # result с await является действием и хранится 1 раз 
        result = await self.session.execute(stmt)
        data = result.scalars().all()
        
        dict_data = []
        for item in data:
            raw_id = item.product_id
            lookup_id = raw_id.strip().upper()
            
            cat = resolve_category(lookup_id)
            main_cat, sub_cat = cat if cat else ("Unknown", "Uncategorized")
            
            dict_data.append({
            "product_id": item.product_id,
            "main_category": main_cat,
            "sub_category": sub_cat,
            "buy_price": item.buy_price,
            "sell_price": item.sell_price,
            "buy_volume": item.buy_volume,
            "sell_volume": item.sell_volume,
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
            cat = resolve_category(pid)
            main_cat, sub_cat = cat if cat else ("Unknown", "Uncategorized")
            display = PRODUCT_ID_TO_DISPLAY.get(
                pid, pid.replace('_', ' ').title(),
            )
            result.append({
                "product_id": pid,
                "display_name": display,
                "main_category": main_cat,
                "sub_category": sub_cat,
                "last_seen": last_seen,
            })
        return result