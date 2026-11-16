"""initial schema

Squashed from:
  8fc446ac7297 (lost)
  6a21c0eef8fa (add identity to id columns)
  bb51d7c23b1f (fix pk to natural keys)

Создаёт таблицы сразу в финальном виде:
  — PK на натуральных ключах, без колонки id
  — tier NOT NULL DEFAULT '' в auction_prices
  — timestamp с серверным дефолтом

Revision ID: bb51d7c23b1f
Revises:
Create Date: 2026-11-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "bb51d7c23b1f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── main_categories ──
    op.create_table(
        "main_categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
    )
    op.create_index(
        "ix_main_categories_name", "main_categories", ["name"], unique=True,
    )

    # ── sub_categories ──
    op.create_table(
        "sub_categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "main_category_id", sa.Integer(),
            sa.ForeignKey("main_categories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(50), nullable=False),
        sa.UniqueConstraint(
            "main_category_id", "name", name="uq_subcat_in_main",
        ),
    )
    op.create_index(
        "ix_sub_categories_main_category_id", "sub_categories", ["main_category_id"],
    )
    op.create_index(
        "ix_sub_categories_name", "sub_categories", ["name"],
    )

    # ── bazaar_prices ── (PK: product_id, timestamp; без id)
    op.create_table(
        "bazaar_prices",
        sa.Column("product_id", sa.String(100), nullable=False),
        sa.Column(
            "sub_category_id", sa.Integer(),
            sa.ForeignKey("sub_categories.id"),
            nullable=False,
        ),
        sa.Column("buy_price", sa.Numeric(16, 2), nullable=False),
        sa.Column("sell_price", sa.Numeric(16, 2), nullable=False),
        sa.Column("buy_volume", sa.Integer(), nullable=False),
        sa.Column("sell_volume", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "product_id", "timestamp", name="bazaar_prices_pkey",
        ),
    )
    op.create_index(
        "ix_bazaar_price_lookup", "bazaar_prices", ["product_id", "timestamp"],
    )
    op.create_index(
        "ix_bazaar_prices_product_id", "bazaar_prices", ["product_id"],
    )
    op.create_index(
        "ix_bazaar_prices_sub_category_id", "bazaar_prices", ["sub_category_id"],
    )

    # ── auction_prices ── (PK: item_name, tier, timestamp; без id)
    op.create_table(
        "auction_prices",
        sa.Column("item_name", sa.String(200), nullable=False),
        sa.Column(
            "tier", sa.String(50), nullable=False,
            server_default=sa.text("''"),
        ),
        sa.Column("lowest_bin", sa.BigInteger(), nullable=False),
        sa.Column(
            "listings_count", sa.Integer(), nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "timestamp", sa.DateTime(timezone=True),
            server_default=sa.text("date_trunc('minute', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "item_name", "tier", "timestamp", name="auction_price_pkey",
        ),
    )
    op.create_index(
        "ix_auction_price_lookup", "auction_prices",
        ["item_name", "tier", "timestamp"],
    )
    op.create_index(
        "ix_auction_prices_item_name", "auction_prices", ["item_name"],
    )
    op.create_index(
        "ix_auction_prices_tier", "auction_prices", ["tier"],
    )

    # ── auction_sales ── (PK: auction_uuid, timestamp; без id)
    op.create_table(
        "auction_sales",
        sa.Column("auction_uuid", sa.String(64), nullable=False),
        sa.Column("item_name", sa.String(200), nullable=False),
        sa.Column("tier", sa.String(50), nullable=True),
        sa.Column("price", sa.BigInteger(), nullable=False),
        sa.Column("bin", sa.Boolean(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "auction_uuid", "timestamp", name="auction_sales_pkey",
        ),
    )
    op.create_index(
        "ix_auction_sale_lookup", "auction_sales",
        ["item_name", "tier", "timestamp"],
    )
    op.create_index(
        "ix_auction_sales_auction_uuid", "auction_sales", ["auction_uuid"],
    )
    op.create_index(
        "ix_auction_sales_item_name", "auction_sales", ["item_name"],
    )
    op.create_index(
        "ix_auction_sales_tier", "auction_sales", ["tier"],
    )


def downgrade() -> None:
    op.drop_table("auction_sales")
    op.drop_table("auction_prices")
    op.drop_table("bazaar_prices")
    op.drop_table("sub_categories")
    op.drop_table("main_categories")