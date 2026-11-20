"""clear_category

Revision ID: 18af4dc9d352
Revises: 53faf3aabb8b
Create Date: 2026-11-20 09:22:42.961001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18af4dc9d352'
down_revision: Union[str, Sequence[str], None] = '53faf3aabb8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('bazaar_prices_sub_category_id_fkey'), 'bazaar_prices', type_='foreignkey')
    op.drop_index(op.f('ix_bazaar_prices_sub_category_id'), table_name='bazaar_prices')
    op.drop_column('bazaar_prices', 'sub_category_id')

    op.drop_index(op.f('ix_sub_categories_main_category_id'), table_name='sub_categories')
    op.drop_index(op.f('ix_sub_categories_name'), table_name='sub_categories')
    op.drop_table('sub_categories')

    op.drop_index(op.f('ix_main_categories_name'), table_name='main_categories')
    op.drop_table('main_categories')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('main_categories',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('main_categories_pkey'))
    )
    op.create_index(op.f('ix_main_categories_name'), 'main_categories', ['name'], unique=True)

    op.create_table('sub_categories',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('main_category_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['main_category_id'], ['main_categories.id'], name=op.f('sub_categories_main_category_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('sub_categories_pkey')),
        sa.UniqueConstraint('main_category_id', 'name', name=op.f('uq_subcat_in_main'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_sub_categories_name'), 'sub_categories', ['name'], unique=False)
    op.create_index(op.f('ix_sub_categories_main_category_id'), 'sub_categories', ['main_category_id'], unique=False)

    op.add_column('bazaar_prices', sa.Column('sub_category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index(op.f('ix_bazaar_prices_sub_category_id'), 'bazaar_prices', ['sub_category_id'], unique=False)
    op.create_foreign_key(op.f('bazaar_prices_sub_category_id_fkey'), 'bazaar_prices', 'sub_categories', ['sub_category_id'], ['id'])
