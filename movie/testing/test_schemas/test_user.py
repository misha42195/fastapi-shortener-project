import os

import pytest


@pytest.mark.skip(
    reason="the scheme is not implemented",
)
def test_user() -> None:
    user_name = {"name": "Misha"}
    assert user_name["name"] == "Sacha"


@pytest.mark.skipif(
    os.name == "nt",
    reason="the test starts only on linux and macos",
)
def test_only_for_linux() -> None:
    on_name = os.name
    print("OS NAME:", on_name)
    assert on_name == "posix"


@pytest.mark.skipif(
    os.name != "nt",
    reason="the test starts only on windows",
)
def test_only_for_windows() -> None:
    os_name = os.name
    assert os_name == "nt"
