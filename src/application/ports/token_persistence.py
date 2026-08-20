from abc import ABC, abstractmethod

from src.application.dto.token_payload import TokenPayloadDTO


class TokenPersistence(ABC):
    @abstractmethod
    async def save(self, dto: TokenPayloadDTO) -> None:
        raise NotImplementedError
