"""
Отдельный процесс-сборщик. Запускается ОДИН раз (без uvicorn).
"""

import asyncio
import logging
import signal

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.config import settings
from core.database import engine
from core.bootstrap import seed_and_cache
from core.hypixel_client import HypixelClient
from core.scheduler import setup_scheduler_jobs
from core.redis_client import redis_pool
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
for noisy in ("httpx", "httpcore", "apscheduler", "sqlalchemy.engine"):
    logging.getLogger(noisy).setLevel(logging.WARNING)
    
log = logging.getLogger("worker")

async def main() -> None:

    await seed_and_cache()
    
  
    client = HypixelClient(settings.hypixel_api_key.get_secret_value())

    scheduler = AsyncIOScheduler()
    setup_scheduler_jobs(scheduler, client)   
    scheduler.start()
    log.info("Worker: планировщик запущен (jobs=%s)", len(scheduler.get_jobs()))
    
    # 4. Graceful shutdown по SIGTERM / SIGINT
    stop = asyncio.Event()
    
    def _handle_signal(sig: int) -> None:
        log.info("Worker: получен сигнал %s, останавливаемся...", sig)
        stop.set()
        
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _handle_signal, sig)
    
    await stop.wait()
    
    scheduler.shutdown(wait=True)
    await redis_pool.disconnect()
    await client.close()
    await engine.dispose()
    log.info("Worker остановлен")
    
if __name__ == "__main__":
    asyncio.run(main())

