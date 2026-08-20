import uuid
from datetime import datetime, timezone, timedelta

from src.application.dto.token_payload import TokenPayloadDTO
from src.application.dto.issued_tokens import IssuedTokensDTO 
from src.application.dto.tokens import TokensDTO 
from src.application.ports.token_provider import TokenProvider


class TokenService:
    def __init__(self, token_provider: TokenProvider):
        self.token_provider = token_provider

    def create_tokens(self, user_id: str) -> IssuedTokensDTO:

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

        return IssuedTokensDTO(
            tokens=tokens,
            refresh_payload=dto_refresh,
        )
