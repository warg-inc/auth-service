from src.setup.grpc_server import GRPCServer
from src.infrastructure.persistence.sqlalchemy.session import create_async_session_factory
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.application.use_cases.create_user import CreateUserUseCase
from src.application.use_cases.login_user import LoginUserUseCase
from src.setup.config.config import get_settings
from src.infrastructure.persistence.sqlalchemy.uow import SqlAlchemyUnitOfWorkFactory
from src.infrastructure.security.jwt_token_service import JWTTokenService

from src.presentation.grpc.controllers.auth_controller import AuthController
from src.application.services.token_service import TokenService

class AppFactory:
    @staticmethod
    def create_grpc_server():
        settings = get_settings()

        session_factory = create_async_session_factory(settings)
        uow_factory = SqlAlchemyUnitOfWorkFactory(session_factory)
        hasher = BcryptPasswordHasher()
        token_provider = JWTTokenService()
        token_service = TokenService(token_provider=token_provider)

        use_case_register_user = CreateUserUseCase(
            hasher=hasher,
            uow_factory=uow_factory
        )
        use_case_login_user = LoginUserUseCase(
            hasher=hasher,
            token_service=token_service,
            uow_factory=uow_factory
        )

        auth_controller = AuthController(
            register_user=use_case_register_user,
            login_user=use_case_login_user
        )
        return GRPCServer(settings, auth_controller)
