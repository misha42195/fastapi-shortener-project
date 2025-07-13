import pytest
from fastapi import status
from starlette.testclient import TestClient


def test_get_view(
    client: TestClient,
) -> None:
    # TODO fake name
    name = "Misha"
    query = {"name": name}
    response = client.get("/", params=query)
    actual_response = response.json()["message"]
    expected_results = f"Hello {name}"

    assert response.status_code == status.HTTP_200_OK, response.text
    assert actual_response == expected_results


@pytest.mark.parametrize(
    "name",
    [
        "Misha",
        "123456",
        "!@#$%^&",
        "ddd",
    ],
)
def test_get_view_custom_names(
    name: str,
    client: TestClient,
) -> None:

    query = {"name": name}
    response = client.get("/", params=query)
    actual_response = response.json()["message"]
    expected_response = f"Hello {name}"
    assert actual_response == expected_response
