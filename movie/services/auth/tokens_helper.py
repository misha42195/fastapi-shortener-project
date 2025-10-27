__all__ = ("AbstractRedisToken",)
import secrets
from abc import ABC, abstractmethod


class AbstractRedisToken(ABC):
    """
    - проверка наличия токена;
    - добавление токена в хранилище;
    - генерация нового токена;
    """

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self) -> str | None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Получение списка токенов из базы
        """

    @abstractmethod
    def delete_token(self, token: str) -> bool:
        """
        Удаление токена из базы
        """
