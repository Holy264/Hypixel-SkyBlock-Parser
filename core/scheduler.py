from functools import wraps
import uuid

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.config import settings
from core.database import async_session
from core.hypixel_client import HypixelClient
from core.redis_client import get_redis
from repositories.bazaar_repo import BazaarRepository
from repositories.auction_repo import AuctionRepository
from services.bazaar_service import BazaarService
from services.auction_service import AuctionService
import logging

log = logging.getLogger(__name__)

LOCK_TTL = 900

def with_redis_lock(lock_name: str):
    """Декоратор для предотвращения одновременного запуска функции через Redis Lock."""
    def decorator(func):
        @wraps(func) 
        async def wrapper(*args, **kwargs):
            r = get_redis()
            token = uuid.uuid4().hex
            key = f"lock:{lock_name}"
            
            ok = await r.set(key, token, nx=True, ex=LOCK_TTL)
            if not ok:
                log.warning("[lock] %s занят, пропуск итерации", lock_name)
                return
            try:
                return await func(*args, **kwargs)
            finally:
                 await r.eval(
                    "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) end",
                    1, key, token,
                )
        return wrapper
    return decorator

@with_redis_lock("bazaar")
async def run_bazaar_sync(client: HypixelClient) -> None:
    async with async_session() as session:
        await BazaarService(client, BazaarRepository(session)).fetch_and_save()

@with_redis_lock("auction")
async def run_auction_sync(client: HypixelClient) -> None:
    async with async_session() as session:
        await AuctionService(client, AuctionRepository(session)).fetch_and_save()

@with_redis_lock("sales")
async def run_sales_sync(client: HypixelClient) -> None:
    try:
        async with async_session() as session:
            saved = await AuctionService(
                client, AuctionRepository(session)
            ).fetch_and_save_sales()
            log.info("[sales] сохранено записей: %d", saved or 0)
    except Exception:
        log.exception("[sales] ошибка синхронизации")


def setup_scheduler_jobs(scheduler: AsyncIOScheduler, client: HypixelClient) -> None:
    scheduler.add_job(run_bazaar_sync,  "interval", args=[client],
                      seconds=settings.bazaar_fetch_interval,
                      id="bazaar_fetch",  replace_existing=True,
                      max_instances=1, coalesce=True, misfire_grace_time=60)
    scheduler.add_job(run_auction_sync, "interval", args=[client],
                      seconds=settings.auction_fetch_interval,
                      id="auction_fetch", replace_existing=True,
                      max_instances=1, coalesce=True, misfire_grace_time=60)
    scheduler.add_job(run_sales_sync,   "interval", args=[client],
                      seconds=settings.sales_fetch_interval,
                      id="sales_fetch",   replace_existing=True,
                      max_instances=1, coalesce=True, misfire_grace_time=60)