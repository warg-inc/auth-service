import datetime
from time import timezone
from typing import Optional

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.password_hasher import PasswordHasher
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_object.user.email import Email
from src.infrastructure.persistence.sqlalchemy.models.users import Users


class UserSqlalchemyRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(Users).
            where(Users.id == user_id)
        )
        user: Users = result.scalar_one_or_none()

        if user is None:
            return None

        return User(email=Email(user.email), surname=user.surname, name=user.name, password=None)

    async def get_by_email(self, email: Email) -> Optional[User]:
        result = await self.session.execute(
            select(Users).
            where(Users.email == email.value)
        )

        user: Users = result.scalar_one_or_none()

        if user is None:
            return None

        return User(email=Email(user.email), surname=user.surname, name=user.name, hashed_password=user.hashed_password)

    async def add(self, data: User) -> None:
        provider = "fitapp"
        user = Users(
            email=data.email.value,
            name=data.name,
            surname=data.surname,
            hashed_password=data.hashed_password,
            provider=provider,
        )

        self.session.add(user)

    async def exists_by_email(self, email: Email) -> bool:
        stmt = select(
            exists().where(Users.email == email.value)
        )
        result = await self.session.execute(stmt)

        return result.scalar()