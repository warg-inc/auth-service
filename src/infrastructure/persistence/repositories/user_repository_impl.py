from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    async def get_by_id(self, user_id: str) -> User:
        return User(user_id="1", name="Vitaliy")