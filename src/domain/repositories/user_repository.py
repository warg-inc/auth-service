from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User
from src.domain.value_object.user.email import Email


class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    async def get_by_email(self, email: Email) -> Optional[User]:
        raise NotImplementedError

    async def add(self, user: User) -> None:
        raise NotImplementedError

    async def exists_by_email(self, email: Email) -> bool:
        raise NotImplementedError
