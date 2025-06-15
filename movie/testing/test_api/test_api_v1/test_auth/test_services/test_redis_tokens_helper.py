from os import getenv
from unittest import TestCase

from api.api_v1.auth.services import redis_tokens

if getenv("TESTING") != "1":
    raise OSError("It is impossible to conduct tests.")


class RedisTokenTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        "проверка создания и сохранения нового токена"
        result = redis_tokens.add_token()
        expected = True
        expected_result = redis_tokens.token_exists(result)
        self.assertEqual(expected_result, expected)


"Test for creating and checking the availability of token in the database"
