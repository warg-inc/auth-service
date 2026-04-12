from dataclasses import dataclass
from datetime import datetime, timezone

from src.application.exceptions.auth_exceptions import InvalidTokenError


@dataclass(frozen=True, slots=True)
class TokenPayloadDTO:

    sub: str
    jti: str
    iat: datetime
    exp: datetime
    type: str

    def to_dict(self):
        return {
            "sub": self.sub,
            "jti": self.jti,
            "iat": int(self.iat.timestamp()),
            "exp": int(self.exp.timestamp()),
            "type": self.type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> TokenPayloadDTO:
        iat = datetime.fromtimestamp(data["iat"], tz=timezone.utc)
        exp = datetime.fromtimestamp(data["exp"], tz=timezone.utc)

        if exp <= iat:
            raise InvalidTokenError()

        return cls(
            sub=data["sub"],
            jti=data["jti"],
            type=data["type"],
            iat=iat,
            exp=exp
        )