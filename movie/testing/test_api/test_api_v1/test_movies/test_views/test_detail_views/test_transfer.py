from email.policy import strict

import pytest
from fastapi.testclient import TestClient
from fastapi import status

from main import app


@pytest.mark.xfail(
    reason="waiting for another response from the server",
    raises=NotImplementedError,
    # strict=False,
)
@pytest.mark.apitest
def test_transfer_movie(
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "transfer_movie",
        slug="some-slug",
    )
    print(url)
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK, response.text
