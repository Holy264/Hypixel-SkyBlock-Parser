from datetime import datetime
from decimal import Decimal
from sqlalchemy import BigInteger, ForeignKey, Identity, Index, Numeric, PrimaryKeyConstraint, String, Integer, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class BazaarPrice(Base):
    __tablename__ = 'bazaar_prices'
    
    product_id: Mapped[str] = mapped_column(String(100))
    buy_price: Mapped[Decimal] = mapped_column(Numeric(16, 2)) 
    sell_price: Mapped[Decimal] = mapped_column(Numeric(16, 2))
    buy_volume: Mapped[int] = mapped_column(Integer)
    sell_volume: Mapped[int] = mapped_column(Integer)
    buy_moving_week: Mapped[int] = mapped_column(Integer, server_default="0")
    sell_moving_week: Mapped[int] = mapped_column(Integer, server_default="0")
    buy_orders: Mapped[int] = mapped_column(Integer, server_default="0")
    sell_orders: Mapped[int] = mapped_column(Integer, server_default="0")
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'timestamp', name='bazaar_prices_pkey'),
        Index('ix_bazaar_price_lookup', 'product_id', 'timestamp'),
        Index('ix_bazaar_prices_product_id', 'product_id'),
    )
    
class AuctionPrice(Base):
    __tablename__ = 'auction_prices'
    
    item_name: Mapped[str] = mapped_column(String(200))
    tier: Mapped[str | None] = mapped_column(String(50), nullable=False, default='', server_default='')
    lowest_bin: Mapped[int] = mapped_column(BigInteger)
    listings_count: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.date_trunc('minute', func.now()), index = True)
    
    __table_args__ = (
        PrimaryKeyConstraint('item_name', 'tier', 'timestamp', name='auction_price_pkey'),
        Index('ix_auction_price_lookup', 'item_name', 'tier', 'timestamp'),
        Index('ix_auction_prices_item_name', 'item_name'),
        Index('ix_auction_prices_tier', 'tier'),
    )

class AuctionSale(Base):
    """Факт продажи — источник средней цены продажи и количества покупок."""
    __tablename__ = 'auction_sales'
    
    auction_uuid: Mapped[str] = mapped_column(String(64), primary_key=True) # индификатор сделки на стороне хайпикселя
    item_name: Mapped[str] = mapped_column(String(200))
    tier: Mapped[str | None] = mapped_column(String(50), nullable=True)
    price: Mapped[int] =  mapped_column(BigInteger)
    bin: Mapped[bool] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('ix_auction_sale_lookup', 'item_name', 'tier', 'timestamp'),
        Index('ix_auction_sales_auction_uuid', 'auction_uuid'),   
        Index('ix_auction_sales_item_name', 'item_name'),
        Index('ix_auction_sales_tier', 'tier'),
    )