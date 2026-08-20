import grpc
import traceback

from src.application.exceptions.user_exceptions import UserAlreadyExistsError
from src.application.use_cases.create_user import CreateUserUseCase
from src.domain.value_object.user.email import Email
from src.domain.value_object.user.password import Password
from src.domain.value_object.user.error.invalid_email_error import InvalidEmailError
from src.domain.value_object.user.error.invalid_password_error import InvalidPasswordError
from src.protos.generated import auth_pb2_grpc, auth_pb2


class AuthController(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self, register_user: CreateUserUseCase):
        self.register_user = register_user

    async def RegisterUser(self, request: auth_pb2.RegisterRequest, context) -> auth_pb2.RegisterResponse:
        try:
            await self.register_user(
                email=Email(request.email),
                surname=request.surname,
                name=request.name,
                password=Password(request.password),
            )

            return auth_pb2.RegisterResponse(success=True)

        except UserAlreadyExistsError:
            await context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                "User already exists"
            )

        except (InvalidEmailError, InvalidPasswordError) as e:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                str(e)
            )

        except Exception as e:
            traceback.print_exc()

            await context.abort(
                grpc.StatusCode.INTERNAL,
                "Internal server error"
            )