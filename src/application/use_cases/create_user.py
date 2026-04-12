from dataclasses import dataclass

from src.application.exceptions.user_exceptions import UserAlreadyExistsError
from src.application.ports.password_hasher import PasswordHasher
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_object.user.email import Email
from src.domain.value_object.user.password import Password


@dataclass(frozen=True)
class CreateUserUseCase:
    repo: UserRepository
    hasher: PasswordHasher

    async def __call__(self, email: Email, surname: str, name: str, password: Password) -> None:
        if await self.repo.exists_by_email(email):
            print(1)
            raise UserAlreadyExistsError()

        hashed = self.hasher.hash(password.value)

        user = User(
            email=email,
            surname=surname,
            name=name,
            hashed_password=hashed
        )

        await self.repo.add(user)

