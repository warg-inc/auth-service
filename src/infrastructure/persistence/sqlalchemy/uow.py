from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.persistence.repositories.jwt_token_sqlalchemy_repository import JWTTokenSqlalchemyRepository
from src.infrastructure.persistence.repositories.user_repository import UserSqlalchemyRepository


class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None
        self._users: UserSqlalchemyRepository | None = None
        self._tokens: JWTTokenSqlalchemyRepository | None = None

    async def __aenter__(self):
        self._session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session is None:
            return

        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            self._session = None
            self._users = None
            self._tokens = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "Сессия не инициализирована. Используйте: 'async with UnitOfWork(...):'"
            )
        return self._session

    @property
    def tokens(self) -> JWTTokenSqlalchemyRepository:
        if self._tokens is None:
            self._tokens = JWTTokenSqlalchemyRepository(self.session)
        return self._tokens

    @property
    def users(self) -> UserSqlalchemyRepository:
        if self._users is None:
            self._users = UserSqlalchemyRepository(self.session)
        return self._users


class UnitOfWorkFactory:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __call__(self):
        return UnitOfWork(self.session_factory)