from grpc import aio
from grpc_reflection.v1alpha import reflection

from src.infrastructure.persistence.sqlalchemy.session import create_async_session_factory
from src.infrastructure.persistence.sqlalchemy.uow import UnitOfWorkFactory
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.presentation.grpc.controllers.auth_controller import AuthController
from src.protos.generated.auth_pb2_grpc import add_AuthServiceServicer_to_server
from src.setup.config.config import Settings, get_settings


class GRPCServer:

    def __init__(self, settings: Settings):
        self.server = aio.server()
        self.settings = settings
        self.server.add_insecure_port("0.0.0.0:50051")

    async def start(self):
        session_factory = create_async_session_factory(self.settings)

        uow_factory = UnitOfWorkFactory(session_factory)

        hasher = BcryptPasswordHasher()

        auth_controller = AuthController(uow_factory, hasher)

        add_AuthServiceServicer_to_server(auth_controller, self.server)

        await self.server.start()
        print("gRPC server running on :50051")

        await self.server.wait_for_termination()
