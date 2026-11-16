from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import engine
from core.redis_client import redis_pool


from api.routes import bazaar, auction, categories
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.hypixel_api_key:
        log.warning("HYPIXEL_API_KEY не задан — возможен rate limit 429")
    
    try:
        yield
    finally:
        await redis_pool.disconnect()
        await engine.dispose()
        log.info("Остановлено") 

app = FastAPI(lifespan=lifespan)
app.include_router(bazaar.router)
app.include_router(auction.router)
app.include_router(categories.router)   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/health")
def read_root():
    return {
        "status": "online",
        "project": "Hupy - Hypixel SkyBlock Parser",
        "docs": "/docs",
    }


# http://localhost:8000/docs

# docker compose up --build app worker