from abc import (
    ABC,
    abstractmethod,
)


class AbstractUsersHelper(ABC):
    """
    - получение пароля по имени пользователя или ничего
    - проверка полученного пароля из базы с тем, что прислал пользователь
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """

        :param username: - имя пользователя
        :type username: - str
        :return: - пароль если он получен
        :rtype:  - str
        """

    @classmethod
    def validate_password(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        return password1 == password2

    def validate_password_match(
        self,
        username: str,
        password: str,
    ) -> bool:
        password_db = self.get_user_password(
            username=username,
        )
        if password_db is None:
            return False
        return self.validate_password(
            password1=password_db,
            password2=password,
        )
