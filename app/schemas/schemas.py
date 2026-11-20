from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.enums import Tier

# ═══════════════════════════════════════════════════════════════════
# BAZAAR
# ═══════════════════════════════════════════════════════════════════
class BazaarHistoryResponse(BaseModel):
    """Одна точка истории цен Bazaar."""

    model_config = ConfigDict(from_attributes=True)

    product_id: str
    buy_price: Decimal
    sell_price: Decimal
    buy_volume: int  
    sell_volume: int 
    buy_moving_week: int # объем покупок за неделю 
    sell_moving_week: int
    buy_orders: int 
    sell_orders: int
    timestamp: datetime

# ═══════════════════════════════════════════════════════════════════
# AUCTION
# ═══════════════════════════════════════════════════════════════════
class AuctionHistoryResponse(BaseModel):
    """Одна точка истории lowest BIN аукциона."""

    model_config = ConfigDict(from_attributes=True)

    item_name: str
    tier: Tier | None
    lowest_bin: int = 0
    listings_count: int = 0 
    timestamp: datetime
    
class AuctionStatsResponse(BaseModel):
    item_name: str
    tier: Tier | None
    available_tiers: list[str]
    period_days: int
    avg_sale_price: int | None   
    sales_count: int
    avg_listings: float | None

    
# эндпоинта поиска
class BazaarItemOut(BaseModel):
    product_id: str # product_id: CARROT_ITEM
    display_name: str # Carrot
    main_category: str | None
    sub_category: str | None
    last_seen: datetime | None
    
class AuctionItemOut(BaseModel):
    item_name: str
    tier: Tier | None
    last_seen: datetime | None