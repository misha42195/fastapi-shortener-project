import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app


@pytest.mark.xfail(
    reason="waiting for another response from the server",
    raises=NotImplementedError,
    strict=False,
)
@pytest.mark.apitest
def test_transfer_movie(
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "transfer_movie",
        slug="some-slug",
    )
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK, response.text
