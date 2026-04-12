import datetime
from sqlalchemy import Column, String, Text, DateTime, UniqueConstraint, Boolean, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import Annotated

from src.infrastructure.persistence.sqlalchemy.base import Base

int_pk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())"), nullable=False)]



class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]

    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    hashed_password: Mapped[str | None] = mapped_column(Text)

    provider: Mapped[str] = mapped_column(String(20))
    provider_sub: Mapped[str | None] = mapped_column(String(50), index=True)

    name: Mapped[str | None] = mapped_column(String(100))
    surname: Mapped[str | None] = mapped_column(String(100))
    picture: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[created_at]
    last_login_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    refresh_tokens = relationship(
        "RefreshTokens",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint('provider', 'provider_sub', name='uq_provider_provider_sub'),
    )