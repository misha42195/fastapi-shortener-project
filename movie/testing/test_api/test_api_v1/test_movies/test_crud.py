import random
from unittest import TestCase


def total(a: int, b: int) -> int:
    return a + b


class TotalTestCase(TestCase):
    def test_total(self) -> None:
        num_a = random.randrange(1, 100)
        num_b = random.randrange(1, 100)

        result = total(num_a, num_b)
        expected_result = num_a + num_b

        print(expected_result)
        self.assertEqual(result, expected_result)
