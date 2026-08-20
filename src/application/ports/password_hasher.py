from abc import ABC, abstractmethod

from src.domain.value_object.user.password import Password


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: Password) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def verify(self, password: Password, password_hash: str) -> bool:
        raise NotImplementedError
