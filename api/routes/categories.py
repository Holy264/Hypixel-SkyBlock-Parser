# api/routes/categories.py
import json

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.redis_client import get_redis
from core.database import get_session
from models.category import MainCategory
from schemas.schemas import MainCategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[MainCategoryOut])
async def list_categories(session: AsyncSession = Depends(get_session)):
    """Отдаёт дерево: main → subcategories. Пример:
    [
      {"id": 1, "name": "Farming", "subcategories": [{"id": 20, "name": "Carrot"}, ...]},
      ...
    ]
    """
    r = get_redis()
    key = "categories:tree"  # Ключ статичный, так как параметров у запроса нет
    
    if (cached := await r.get(key)):
      return json.loads(cached)
    stmt = (
        select(MainCategory)
        .options(selectinload(MainCategory.subcategories))
        .order_by(MainCategory.name)
    )
    categories = (await session.execute(stmt)).scalars().all()
    
    validated = [MainCategoryOut.model_validate(c) for c in categories]
    payload = json.dumps([v.model_dump(mode="json") for v in validated])
    await r.set(key, payload, ex=3600)
    return validated