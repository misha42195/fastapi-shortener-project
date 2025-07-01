from os import getenv

import pytest

if getenv("TESTING") != "1":
    pytest.exit("The environment is not ready for tests")
