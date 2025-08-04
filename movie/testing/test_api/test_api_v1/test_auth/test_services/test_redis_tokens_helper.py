from unittest import TestCase

from api.api_v1.auth.services import redis_tokens


class RedisTokenTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        """проверка создания и сохранения нового токена"""
        result = redis_tokens.add_token()
        self.assertTrue(result)
