import json

from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.enums import Tier
from core.redis_client import get_redis
from schemas.schemas import AuctionItemOut, AuctionStatsResponse, AuctionHistoryResponse
from api.dependencies import get_auction_repo
from repositories.auction_repo import AuctionRepository
from core.utils.normalize_item_name import normalize_item_name

router = APIRouter(prefix="/auction", tags=["auction"])


@router.get("/search", response_model=list[AuctionItemOut])
async def search_auction(
    search: str = Query("", max_length=200),
    limit: int = Query(20, ge=1, le=100),
    repo: AuctionRepository = Depends(get_auction_repo),
    ):
    """Автокомплит по auction-предметам."""
    s = search.strip().lower()
    key = f"auction:search:{s}:{limit}"

    r = get_redis()
    if (cached := await r.get(key)):
        return json.loads(cached)

    data = await repo.search_items(s, limit)
    validated = [AuctionItemOut.model_validate(row) for row in data]
    payload = json.dumps([v.model_dump(mode="json") for v in validated])
    await r.set(key, payload, ex=60)
    return validated


@router.get("/history", response_model=list[AuctionHistoryResponse])
async def get_auction_history(
    item_name: str = Query(..., min_length=1, max_length=200),
    tier: Tier | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    repo: AuctionRepository = Depends(get_auction_repo),
    ):
    # ключ кэша — по нормализованному имени, чтобы "Hyperion" и "hyperion "
    # (с пробелом) не создавали дубликаты
    norm = normalize_item_name(item_name).lower()
    key = f"auction:history:{norm}:{tier}:{limit}"

    r = get_redis()
    if (cached := await r.get(key)):
        return json.loads(cached)

    data = await repo.get_history(item_name, tier, limit)
    validated = [AuctionHistoryResponse.model_validate(row) for row in data]
    payload = json.dumps([v.model_dump(mode="json") for v in validated])
    await r.set(key, payload, ex=60)
    return validated


@router.get("/stats", response_model=AuctionStatsResponse)
async def get_auction_stats(
    item_name: str = Query(..., min_length=1, max_length=200),
    tier: Tier | None = Query(None),
    days: int = Query(7, ge=1, le=90),
    repo: AuctionRepository = Depends(get_auction_repo),
):
    norm = normalize_item_name(item_name).lower()
    key = f"auction:stats:{norm}:{tier}:{days}"

    r = get_redis()
    if (cached := await r.get(key)):
        return json.loads(cached)

    try:
        data = await repo.get_stats(item_name, tier, days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    validated = AuctionStatsResponse.model_validate(data)
    payload = json.dumps(validated.model_dump(mode="json"))
    await r.set(key, payload, ex=60)
    return validated