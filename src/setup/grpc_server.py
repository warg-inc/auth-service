from grpc import aio

from src.setup.config.config import Settings
from src.presentation.grpc.controllers.auth_controller import AuthController
from src.protos.generated.auth_pb2_grpc import add_AuthServiceServicer_to_server


class GRPCServer:

    def __init__(self, settings: Settings, auth_controller: AuthController):
        self.server = aio.server()
        self.settings = settings
        self.server.add_insecure_port(f"{settings.grpc_host}:{settings.grpc_port}")
        self.auth_controller = auth_controller

    async def start(self):
        add_AuthServiceServicer_to_server(self.auth_controller, self.server)

        await self.server.start()
        print("gRPC server running on :50051")

        await self.server.wait_for_termination()
