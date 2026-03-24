from uuid import UUID

import grpc
from src.protos.generated import user_pb2, user_pb2_grpc



class UserController(user_pb2_grpc.UserServiceServicer):

    def __init__(self, get_user_use_case):
        self.get_user_use_case = get_user_use_case

    async def GetUser(
            self,
            request: user_pb2.GetUserRequest,
            context: grpc.ServicerContext
    ) -> user_pb2.GetUserResponse:

        user = await self.get_user_use_case(request.user_id)
        return user_pb2.GetUserResponse(
            user_id=user.id,
            name=user.name,
        )


