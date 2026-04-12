import uuid
from datetime import datetime, timezone, timedelta

import jwt

from src.application.dto.token_payload import TokenPayloadDTO
from src.application.dto.tokens import TokensDTO
from src.application.exceptions.auth_exceptions import *
from src.application.ports.token_provider import TokenProvider



class JWTTokenService(TokenProvider):
    def create(self, dto_access: TokenPayloadDTO, dto_refresh: TokenPayloadDTO) -> TokensDTO:

        access_token = jwt.encode(
            dto_access.to_dict(),
            'settings.JWT_PRIVATE_KEY',
            algorithm="HS256",
        )

        refresh_token = jwt.encode(
            dto_refresh.to_dict(),
            'settings.JWT_PRIVATE_KEY',
            algorithm="HS256",
        )

        return TokensDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def verify_access_token(self, token: str) -> TokenPayloadDTO:
        try:
            payload = jwt.decode(
                token,
                'settings.JWT_PRIVATE_KEY',
                algorithms=["HS256"],
                options={"require": ["exp", "iat", "sub", "jti", "type"]}
            )

            if payload.get("type") != "access":
                raise InvalidTokenTypeError()

            dto = TokenPayloadDTO.from_dict(payload)
            now = datetime.now(timezone.utc)

            if dto.iat > now:
                raise InvalidTokenError()

            return dto

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()

        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    def verify_refresh_token(self, token: str) -> TokenPayloadDTO:
        try:
            payload = jwt.decode(
                token,
                'settings.JWT_PRIVATE_KEY',
                algorithms=["HS256"],
                options={"require": ["exp", "iat", "sub", "jti", "type"]},
            )

            if payload.get("type") != "refresh":
                raise InvalidTokenTypeError()

            dto = TokenPayloadDTO.from_dict(payload)
            now = datetime.now(timezone.utc)

            if dto.iat > now:
                raise InvalidTokenError()

            return dto

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()

        except jwt.InvalidTokenError:
            raise InvalidTokenError()
