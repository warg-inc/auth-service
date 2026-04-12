from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.application.dto.token_payload import TokenPayloadDTO
from src.application.ports.token_persistence import TokenPersistence
from src.infrastructure.persistence.sqlalchemy.models.refresh_token import RefreshTokens


class JWTTokenSqlalchemyRepository(TokenPersistence):
    def __init__(self, session: AsyncSession):
        self.session = session

    def save(self, dto: TokenPayloadDTO) -> None:
        refresh_tokens = RefreshTokens(
            jti=uuid.UUID(dto.jti),
            user_id=int(dto.sub),
            issued_at=dto.iat,
            expires_at=dto.exp,
            revoked=False,
        )

        self.session.add(refresh_tokens)
        self.session.refresh(refresh_tokens)

