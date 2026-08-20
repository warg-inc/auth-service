
class UserError(Exception):
    def __init__(self, message: str = "User error", code: str = "user_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class UserAlreadyExistsError(UserError):
    def __init__(self):
        super().__init__(message="User Already Exists", code="user_exists")

class InvalidCredentialsError(UserError):
    def __init__(self, message = "Invalid Credentials Error", code = "invalid_credentials"):
        super().__init__(message, code)