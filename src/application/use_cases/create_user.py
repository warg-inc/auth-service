from dataclasses import dataclass

from src.application.exceptions.user_exceptions import UserAlreadyExistsError
from src.application.ports.password_hasher import PasswordHasher
from src.application.ports.uow_interface import UnitOfWorkFactory
from src.domain.entities.user import User
from src.domain.value_object.user.email import Email
from src.domain.value_object.user.password import Password


@dataclass(frozen=True)
class CreateUserUseCase:
    hasher: PasswordHasher
    uow_factory: UnitOfWorkFactory

    async def __call__(self, email: Email, surname: str, name: str, password: Password) -> None:
        async with self.uow_factory() as uow:
            if await uow.users.exists_by_email(email):
                raise UserAlreadyExistsError()

            hashed = self.hasher.hash(password)

            user = User(
                email=email,
                surname=surname,
                name=name,
                hashed_password=hashed
            )

            await uow.users.add(user)

