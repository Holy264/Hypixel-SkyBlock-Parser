import logging

from core.database import async_session
from services.categories_service import CategoryService
from core.category_cache import build_category_cache

log = logging.getLogger(__name__)

async def seed_and_cache() -> None:
    async with async_session() as session:
        await CategoryService(session).seed_categories()
        await build_category_cache(session)
    log.info("Категории засеяны, кэш построен")
