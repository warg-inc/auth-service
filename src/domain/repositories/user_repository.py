from abc import ABC, abstractmethod
from src.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User:
        pass