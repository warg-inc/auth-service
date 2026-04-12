class TokenError(Exception):
    def __init__(self, message: str = "Token error", code: str = "token_error"):
        self.message = message
        self.code = code
        super().__init__(message)

class TokenExpiredError(TokenError):
    def __init__(self):
        super().__init__(
            message="Token has expired",
            code="token_expired"
        )

class InvalidTokenError(TokenError):
    def __init__(self):
        super().__init__(
            message="Invalid token",
            code="invalid_token"
        )

class InvalidTokenTypeError(TokenError):
    def __init__(self):
        super().__init__(
            message="Invalid token type",
            code="invalid_token_type"
        )