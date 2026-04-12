from abc import ABC, abstractmethod

from src.application.dto.token_payload import TokenPayloadDTO
from src.application.dto.tokens import TokensDTO


class TokenProvider(ABC):
    @abstractmethod
    def create(self, dto_access: TokenPayloadDTO, dto_refresh) -> TokensDTO:
        raise NotImplementedError

    @abstractmethod
    def verify_access_token(self, token: str) -> TokenPayloadDTO:
        raise NotImplementedError

    @abstractmethod
    def verify_refresh_token(self, token: str) -> TokenPayloadDTO:
        raise NotImplementedError