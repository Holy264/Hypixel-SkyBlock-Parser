import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context

from core.config import settings
from core.database import Base
from models import *  # noqa: F401

config = context.config


target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
config.set_main_option("sqlalchemy.url", settings.database_url)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    """Синхронный контекст выполнения миграций внутри асинхронного соединения."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Асинхронный запуск миграций с использованием async_engine_from_config."""
    
    
    section = config.get_section(config.config_ini_section, {})
    
    # ВАЖНО: принудительно прописываем URL из настроек в словарь конфигурации, 
    # чтобы async_engine_from_config увидел актуальную строку подключения
    section["sqlalchemy.url"] = settings.database_url


    connectable = async_engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
