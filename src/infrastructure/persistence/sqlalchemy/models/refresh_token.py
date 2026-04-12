import datetime

from sqlalchemy import DateTime, select, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import Annotated

from src.infrastructure.persistence.sqlalchemy.base import Base

int_pk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())"), nullable=False)]

class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int_pk]
    jti: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    issued_at: Mapped[created_at]
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user = relationship("Users", back_populates="refresh_tokens")
