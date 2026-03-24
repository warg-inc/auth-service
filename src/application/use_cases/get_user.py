from dataclasses import dataclass

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


@dataclass(frozen=True)
class GetUserUseCase:
    user_repo: UserRepository

    async def __call__(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        return user