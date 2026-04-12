from src.application.use_cases.get_user import GetUserUseCase
from src.infrastructure.persistence.repositories.user_repository import UserSqlalchemyRepository
from src.presentation.grpc.controllers.user_controller import UserController
from src.setup.grpc_server import GRPCServer
from src.setup.config.config import get_settings
from src.infrastructure.persistence.sqlalchemy.session import create_async_session_factory


class AppFactory:
    @staticmethod
    def create_grpc_server():
        settings = get_settings()

        return GRPCServer(settings)