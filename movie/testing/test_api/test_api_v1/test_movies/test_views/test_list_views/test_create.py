import logging
from typing import Any

import httpx
import pytest
from _pytest.fixtures import SubRequest
from _pytest.logging import LogCaptureFixture
from starlette import status
from starlette.testclient import TestClient

from main import app
from schemas.muvies import CreateMovies, Movies
from testing.conftest import build_movie_create_random_slug


@pytest.mark.apitest
def test_create_movie(
    auth_client: TestClient,
    caplog: LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    url = app.url_path_for("create_movie")
    data: dict[str, str] = build_movie_create_random_slug().model_dump(mode="json")
    response: httpx.Response = auth_client.post(url=url, json=data)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert data["title"] == response_data["title"], response.text
    assert data["description"] == response_data["description"], response.text
    assert data["release_year"] == response_data["release_year"], response.text
    assert data["director"] == response_data["director"], response.text
    assert data["slug"] == response_data["slug"], response.text

    assert "Создание нового фильма" in caplog.text
    assert data["slug"] in caplog.text


@pytest.mark.apitest
def test_create_movie_already_exists(
    auth_client: TestClient,
    movie: Movies,
) -> None:
    url = app.url_path_for("create_movie")
    data = CreateMovies.model_dump(movie, mode="json")
    response = auth_client.post(
        url=url,
        json=data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    assert (
        f"Movie with slug='{movie.slug}' already exists." == response.json()["detail"]
    )


@pytest.mark.apitest
class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(
                ("ab", "string_too_short", "String should have at least 3 characters"),
                id="short slug",
            ),
            pytest.param(
                (
                    "to-long-slug",
                    "string_too_long",
                    "String should have at most 10 characters",
                ),
                id="long slug",
            ),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str, str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, ext_type, expected_msg = request.param
        data["slug"] = slug
        return (
            data,
            ext_type,
            expected_msg,
        )

    def test_invalid_slug(
        self,
        movie_create_values: CreateMovies,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_movie")
        create_data, expected_type, expected_msg = movie_create_values
        response = auth_client.post(url=url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error = response.json()["detail"][0]
        assert error["type"] == expected_type
        assert error["msg"] == expected_msg
