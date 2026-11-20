from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    hypixel_api_key: SecretStr = SecretStr('')
    database_url: str = "postgresql+asyncpg://skyblock:skyblock@localhost:5432/skyblock"
    redis_url: str = "redis://localhost:6379/0"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False
    bazaar_fetch_interval: int = 300 
    auction_fetch_interval: int = 300 
    sales_fetch_interval: int = 120
    
    # проверяет данные в env
    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",  
    )

settings = Settings()