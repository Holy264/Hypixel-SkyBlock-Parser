from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.category import MainCategory, SubCategory

# (main_name, sub_name) -> sub_category_id
SUB_CATEGORY_CACHE: dict[tuple[str, str], int] = {}

FALLBACK_KEY = ("Unknown", "Uncategorized")


def get_or_fallback(cat: tuple[str, str] | None) -> int | None:
    """sub_category_id или fallback."""
    if cat is not None:
        sub_id = SUB_CATEGORY_CACHE.get(cat)
        if sub_id is not None:
            return sub_id
    return SUB_CATEGORY_CACHE.get(FALLBACK_KEY)


async def build_category_cache(session: AsyncSession) -> None:
    stmt = (
        select(MainCategory.name, SubCategory.name, SubCategory.id)
        .join(SubCategory, SubCategory.main_category_id == MainCategory.id)
    )
    rows = (await session.execute(stmt)).all()
    SUB_CATEGORY_CACHE.clear()
    SUB_CATEGORY_CACHE.update({(m, s): sid for m, s, sid in rows})
    
    