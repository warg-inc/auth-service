from src.application.use_cases.get_user import GetUserUseCase
from src.infrastructure.persistence.repositories.user_repository_impl import UserRepositoryImpl
from src.presentation.grpc.controllers.user_controller import UserController
from src.setup.grpc_server import GRPCServer


class AppFactory:

    @staticmethod
    def create_grpc_server():
        user_repo = UserRepositoryImpl()

        get_user_use_case = GetUserUseCase(user_repo)

        user_controller = UserController(get_user_use_case)

        return GRPCServer(user_controller)