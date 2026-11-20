from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url, 
                             echo=settings.db_echo,
                             pool_size=settings.db_pool_size,
                             max_overflow=settings.db_max_overflow,
                             pool_pre_ping=True)


async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session