from grpc import aio
from grpc_reflection.v1alpha import reflection

from src.protos.generated import user_pb2_grpc



class GRPCServer:

    def __init__(self, user_controller):
        self.server = aio.server()

        user_pb2_grpc.add_UserServiceServicer_to_server(
            user_controller,
            self.server
        )

        SERVICE_NAMES = (
            user_pb2_grpc.UserServiceServicer.__name__,
            reflection.SERVICE_NAME,
        )

        reflection.enable_server_reflection(SERVICE_NAMES, self.server)

        self.server.add_insecure_port("0.0.0.0:50051")

    async def start(self):
        await self.server.start()
        print("gRPC server running on :50051")