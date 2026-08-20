from __future__ import annotations
from abc import ABC, abstractmethod

from src.application.ports.token_persistence import TokenPersistence
from src.domain.repositories.user_repository import UserRepository

class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> UnitOfWork:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @property
    @abstractmethod
    def tokens(self) -> TokenPersistence:
        raise NotImplementedError

    @property
    @abstractmethod
    def users(self) -> UserRepository:
        raise NotImplementedError


class UnitOfWorkFactory(ABC):
    @abstractmethod
    def __call__(self) -> UnitOfWork:
        raise NotImplementedError
