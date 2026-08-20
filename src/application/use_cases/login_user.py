from dataclasses import dataclass

from src.application.exceptions.user_exceptions import InvalidCredentialsError
from src.application.ports.password_hasher import PasswordHasher
from src.application.ports.uow_interface import UnitOfWorkFactory
from src.domain.value_object.user.email import Email
from src.domain.value_object.user.password import Password
from src.application.services.token_service import TokenService
from src.application.dto.tokens import TokensDTO


@dataclass(frozen=True)
class LoginUserUseCase:
    hasher: PasswordHasher
    token_service: TokenService
    uow_factory: UnitOfWorkFactory

    async def __call__(self, email: Email, password: Password) -> TokensDTO:
        async with self.uow_factory() as uow:
            user = await uow.users.get_by_email(email=email)
            if not user or user.id is None:
                raise InvalidCredentialsError()

            if not self.hasher.verify(password, user.hashed_password):
                raise InvalidCredentialsError()
            
            issued_tokens = self.token_service.create_tokens(user_id=str(user.id))
            await uow.tokens.save(dto=issued_tokens.refresh_payload)

            return issued_tokens.tokens
