import json

from fastapi import APIRouter, Depends, Query
from core.redis_client import get_redis
from core.utils.normalize_product_id import normalize_product_id
from repositories.bazaar_repo import BazaarRepository
from api.dependencies import get_bazaar_repo
from schemas.schemas import BazaarItemOut, BazaarHistoryResponse

router = APIRouter(prefix="/bazaar", tags=["bazaar"])

@router.get("/search", response_model=list[BazaarItemOut])
async def search_bazaar(
    search: str = Query("", max_length=100), 
    limit: int = Query(20, ge=1, le=100),
    repo: BazaarRepository = Depends(get_bazaar_repo),
    ):
    """Автокомплит по bazaar-продуктам. Пустой search → алфавиту."""
    r = get_redis()
    s = search.strip().lower()
    key = f"bazaar:search:{s}:{limit}"
    if (cached := await r.get(key)):
        return json.loads(cached)

    data = await repo.search_products(s, limit)
    validated = [BazaarItemOut.model_validate(row) for row in data]
    await r.set(key, validated, ex=30) 
    return validated


@router.get("/{product_id}/history", response_model=list[BazaarHistoryResponse])
async def get_bazaar_history(
    product_id: str,
    limit: int = Query(100, le=1000),
    repo: BazaarRepository = Depends(get_bazaar_repo),
    ):
    pid = normalize_product_id(product_id)
    key = f"bazaar:{pid}:{limit}"
    r = get_redis()
    if (cached := await r.get(key)):
        return json.loads(cached)
    data = await repo.get_history(pid, limit)
    validated = [BazaarHistoryResponse.model_validate(row) for row in data]
    payload = json.dumps([v.model_dump(mode="json") for v in validated], default=str)
    await r.set(key, payload, ex=30)  
    return validated
