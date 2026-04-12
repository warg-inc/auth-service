from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.setup.config.config import Settings


def create_async_session_factory(settings: Settings) -> async_sessionmaker[AsyncSession]:
    async_engine = create_async_engine(
        settings.db_url,
        echo=settings.db_echo,
        pool_pre_ping=True
    )

    return async_sessionmaker(async_engine, expire_on_commit=False)