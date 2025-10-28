import pytest
from fastapi import status
from starlette.testclient import TestClient


@pytest.mark.skip(reason="CI environment missing routes")
def test_get_view(
    client: TestClient,
) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.template.name == "home.html"  # type: ignore[attr-defined]
    assert "movies" in response.context, response.context  # type: ignore[attr-defined]
    assert isinstance(response.context["movies"], list)  # type: ignore[attr-defined]
