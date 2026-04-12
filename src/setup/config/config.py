from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: str = "5433"
    db_name: str = "users"
    db_user: str = "postgres"
    db_password: str = "1234"
    db_echo: bool = True

    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50051
    grpc_reflection_enabled: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

@lru_cache
def get_settings() -> Settings:
    return Settings()