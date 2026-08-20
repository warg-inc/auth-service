from dataclasses import dataclass

from src.application.dto.tokens import TokensDTO
from src.application.dto.token_payload import TokenPayloadDTO




@dataclass(frozen=True, slots=True)
class IssuedTokensDTO:
    tokens: TokensDTO
    refresh_payload: TokenPayloadDTO
