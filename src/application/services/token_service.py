import uuid
from datetime import datetime, timezone, timedelta

from jwt import jwt

from src.application.dto.token_payload import TokenPayloadDTO
from src.application.dto.tokens import TokensDTO
from src.application.ports.token_persistence import TokenPersistence
from src.application.ports.token_provider import TokenProvider


class TokenService:
    def __init__(self, token_provider: TokenProvider, token_persistence: TokenPersistence):
        self.token_provider = token_provider
        self.token_persistence = token_persistence

    def create_tokens(self, user_id: str):

        now = datetime.now(timezone.utc)
        jti_access = str(uuid.uuid4())
        exp_access = now + timedelta(minutes=1)
        dto_access = TokenPayloadDTO(
            sub=user_id,
            jti=jti_access,
            iat=now,
            exp=exp_access,
            type="access"
        )

        jti_refresh = str(uuid.uuid4())
        exp_refresh = now + timedelta(hours=1)
        dto_refresh = TokenPayloadDTO(
            sub=user_id,
            jti=jti_refresh,
            iat=now,
            exp=exp_refresh,
            type="refresh"
        )

        tokens: TokensDTO = self.token_provider.create(dto_access, dto_refresh)

        self.token_persistence.save()


