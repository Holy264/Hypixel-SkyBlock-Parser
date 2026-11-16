from sqlalchemy.dialects.postgresql import insert as pg_insert

from datetime import datetime, timedelta, timezone
import logging

from sqlalchemy import case, func, select
from repositories.base import Baserepository
from models.price import AuctionPrice, AuctionSale
from core.utils.normalize_item_name import normalize_item_name

logger = logging.getLogger(__name__)


class AuctionRepository(Baserepository):

    async def save_prices(self, prices: list[dict]) -> int:
        """Сохраняет агрегированные lowest BIN.

        prices: [{"item_name": str, "tier": str | None,
                  "lowest_bin": int, "listings_count": int}, ...]

        Если в пачке окажутся две записи с одинаковым (item_name, tier)
        — оставляем запись с минимальным lowest_bin, а listings_count
        складываем.
        """
        if not prices:
            return 0

        merged: dict[tuple[str, str | None], dict] = {}
        for p in prices:
            try:
                item_name = normalize_item_name(p.get("item_name"))
                if not item_name:
                    continue

                tier = p.get("tier")
                tier = str(tier).strip().upper() if tier else ''

                price = int(p["lowest_bin"])
                listings = int(p.get("listings_count") or 0)

                key = (item_name, tier)
                cur = merged.get(key)
                if cur is None:
                    merged[key] = {
                        "item_name": item_name,
                        "tier": tier,
                        "lowest_bin": price,
                        "listings_count": listings,
                    }
                else:
                    cur["lowest_bin"] = min(cur["lowest_bin"], price)
                    cur["listings_count"] += listings

            except (ValueError, TypeError, KeyError) as e:
                logger.warning(
                    "Ошибка валидации цены %r: %s", p.get("item_name"), e,
                )
                continue

        if not merged:
            return 0

        objects = [AuctionPrice(**row) for row in merged.values()]

        try:
            self.session.add_all(objects)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error("Ошибка сохранения цен в БД: %s", e)
            raise

        return len(objects)

    async def get_history(
        self, item_name: str, tier: str | None, limit: int = 100,
    ) -> list[dict]:
        """История lowest BIN. Входное имя нормализуется тем же правилом,
        что и при сохранении.
        """
        item_name = normalize_item_name(item_name)

        stmt = (
            select(AuctionPrice)
            .where(AuctionPrice.item_name == item_name)
            .order_by(AuctionPrice.timestamp.desc())
            .limit(limit)
        )
        if tier:
            stmt = stmt.where(AuctionPrice.tier == tier.strip().upper())

        result = await self.session.execute(stmt)
        data = result.scalars().all()

        return [
            {
                "item_name": item.item_name,
                "tier": item.tier or None,
                "lowest_bin": int(item.lowest_bin) if item.lowest_bin is not None else 0,
                "listings_count": item.listings_count,
                "timestamp": (item.timestamp),
            }
            for item in data
        ]

    # ═══════════════════════════════════════════════════════════
    # SALES
    # ═══════════════════════════════════════════════════════════
    async def save_sales(self, sales: list[dict]) -> int:
        if not sales:
            return 0

        objects: list[AuctionSale] = []
        seen_uuids: set[str] = set()

        for s in sales:
            try:
                uuid = s.get("auction_uuid")
                if not uuid:
                    continue

                item_name = normalize_item_name(s.get("item_name"))
                if not item_name:
                    continue

                if uuid in seen_uuids:
                    continue
                seen_uuids.add(uuid)

                tier = s.get("tier")
                tier = str(tier).strip().upper() if tier else None

                objects.append(AuctionSale(
                    auction_uuid=uuid,
                    item_name=item_name,
                    tier=tier,
                    price=int(s["price"]),
                    bin=bool(s.get("bin", True)),
                ))
            except (ValueError, TypeError, KeyError) as e:
                logger.warning(
                    "Ошибка валидации продажи %r: %s", s.get("item_name"), e,
                )
                continue

        if not objects:
            return 0
        
        rows = [
        {
            "auction_uuid": o.auction_uuid,
            "item_name": o.item_name,
            "tier": o.tier,
            "price": o.price,
            "bin": o.bin,
        }
        for o in objects
    ]
        
        stmt = (
        pg_insert(AuctionSale)
        .values(rows)
        .on_conflict_do_nothing(index_elements=["auction_uuid"])
        .returning(AuctionSale.auction_uuid)
    )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return len(result.scalars().all())

    # ═══════════════════════════════════════════════════════════
    # STATS
    # ═══════════════════════════════════════════════════════════
    async def get_stats(
        self, item_name: str, tier: str | None, days: int = 7,
    ) -> dict:
        item_name = normalize_item_name(item_name)
        tier = tier.strip().upper() if tier else None

        since = datetime.now(timezone.utc) - timedelta(days=days)

        #    Какие редкости вообще есть у предмета за период
        #    Источники: и продажи (auction_sales), и выставления (auction_prices).
        tiers_stmt = (
            select(AuctionSale.tier).where(
                AuctionSale.item_name == item_name,
                AuctionSale.tier.isnot(None),
                AuctionSale.timestamp >= since,
            ).union(
                select(AuctionPrice.tier).where(
                    AuctionPrice.item_name == item_name,
                    AuctionPrice.tier.isnot(None),
                    AuctionPrice.timestamp >= since,
                )
            )
        )
        available_tiers = sorted(
            {r[0] for r in (await self.session.execute(tiers_stmt)).all()}
        )

        if tier is not None and tier not in available_tiers:
            raise ValueError(
                f"tier '{tier}' not found for '{item_name}'. "
                f"Available: {available_tiers}"
            )
            
        detected_tier = tier
        if detected_tier is None and len(available_tiers) == 1:
            detected_tier = available_tiers[0]

        sales_stmt = select(
            func.avg(AuctionSale.price),
            func.count(),
        ).where(
            AuctionSale.item_name == item_name,
            AuctionSale.timestamp >= since,
        )
        if detected_tier:
            sales_stmt = sales_stmt.where(AuctionSale.tier == detected_tier)

        avg_sale_price, sales_count = (
            await self.session.execute(sales_stmt)
        ).one()

        listings_stmt = select(
            func.avg(AuctionPrice.listings_count),
        ).where(
            AuctionPrice.item_name == item_name,
            AuctionPrice.timestamp >= since,
        )
        if detected_tier:
            listings_stmt = listings_stmt.where(AuctionPrice.tier == detected_tier)

        avg_listings = (await self.session.execute(listings_stmt)).scalar()

        return {
            "item_name": item_name,
            "tier": detected_tier or None,
            "available_tiers": available_tiers,
            "period_days": days,
            "avg_sale_price": (
                int(avg_sale_price) if avg_sale_price is not None else None
            ),
            "sales_count": sales_count or 0,
            "avg_listings": (
                float(avg_listings) if avg_listings is not None else None
            ),
        }
    
    async def search_items(self, search: str, limit: int = 20,) -> list[dict]:
        """Поиск auction-предметов по подстроке в item_name.

        Пустой `search` → топ активных.
        """
        since = datetime.now(timezone.utc) - timedelta(days=30)
        s = search.strip().lower()

        stmt = (
            select(
                AuctionPrice.item_name,
                AuctionPrice.tier,
                func.max(AuctionPrice.timestamp).label("last_seen"),
            )
            .where(AuctionPrice.timestamp >= since)
            .group_by(AuctionPrice.item_name, AuctionPrice.tier)
        )

        if s:
            col = func.lower(AuctionPrice.item_name)
            stmt = stmt.where(col.contains(s, autoescape=True))

            rank = case(
                (col == s, 0),
                (col.startswith(s, autoescape=True), 1),
                else_=2,
            )
            stmt = stmt.order_by(
                rank, AuctionPrice.item_name, AuctionPrice.tier,
            )
        else:
            stmt = stmt.order_by(
                AuctionPrice.item_name, AuctionPrice.tier,
            )

        stmt = stmt.limit(limit)
        rows = (await self.session.execute(stmt)).all()
        return [
            {"item_name": n, "tier": t or None, "last_seen": ts}
            for n, t, ts in rows
        ]
        