from abc import (
    ABC,
    abstractmethod,
)


class AbstractUserHelper(ABC):
    """
    - получение пароля по имени пользователя
    - проверка пароля на совпадение с тем что в БД.
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        По переданному имени находит пароль.

        Возвращает пароль, если есть.

        :param username: - имя пользователя.
        :type username: - строка
        :return: - пароль пользователя, если найден
        :rtype: - строка
        """

    @classmethod
    def validate_password_match(
        cls,
        password1: str,
        password2: str,
    ):
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверить, валиден ли пароль.

        :param username: - чей пароль проверяем
        :type username: - строка
        :param password: - переданный пароль, сверить с тем, что в БД.
        :type password: - строка
        :return: - True, если совпадает, иначе False
        :rtype:  - bool
        """
        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.validate_password_match(
            password1=db_password,
            password2=password,
        )
