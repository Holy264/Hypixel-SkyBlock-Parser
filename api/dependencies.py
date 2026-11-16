# Подключение к repo 
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from repositories.bazaar_repo import BazaarRepository
from repositories.auction_repo import AuctionRepository

def get_bazaar_repo(
    session: AsyncSession = Depends(get_session),
) -> BazaarRepository:
    return BazaarRepository(session)

def get_auction_repo(
    session: AsyncSession = Depends(get_session),
) -> AuctionRepository:
    return AuctionRepository(session)