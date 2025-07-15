import random
import string
from datetime import date
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from pydantic import ValidationError
from starlette import status
from starlette.testclient import TestClient

from main import app
from schemas.muvies import CreateMovies, Movie
from testing.conftest import build_movie_create_random_slug


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    data: dict[str, str] = build_movie_create_random_slug().model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert data["title"] == response_data["title"], response.text
    assert data["description"] == response_data["description"], response.text
    assert data["release_year"] == response_data["release_year"], response.text
    assert data["director"] == response_data["director"], response.text
    assert data["slug"] == response_data["slug"], response.text


def test_create_movie_already_exists(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    url = app.url_path_for("create_movie")
    data = CreateMovies.model_dump(
        movie,
        mode="json",
    )
    response = auth_client.post(
        url=url,
        json=data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    assert (
        f"Movie with slug='{movie.slug}' already exists." == response.json()["detail"]
    )


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(
                ("ab", "too short slug"),
                id="short slug",
            ),
            pytest.param(
                ("to-long-slug", "too long slug"),
                id="long slug",
            ),
        ]
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, ext_type = request.param
        print(slug, ext_type)
        data["slug"] = slug
        return (
            data,
            ext_type,
        )

    def test_invalid_slug(
        self,
        movie_create_values,
        auth_client,
    ) -> None:
        url = app.url_path_for("create_movie")
        create_data, ext_error_type = movie_create_values
        response = auth_client.post(url=url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        expected_error_detail = response.json()["detail"][0]
        assert expected_error_detail == ext_error_type
