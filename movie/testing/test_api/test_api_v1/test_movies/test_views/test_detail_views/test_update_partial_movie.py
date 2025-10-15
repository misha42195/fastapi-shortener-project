from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from starlette.testclient import TestClient

from main import app
from schemas.muvies import DESCRIPTION_MAX_LENGTH, DescriptionString, Movies
from storage.movies.crud import movie_storage
from testing.conftest import create_movie_random_slug


class TestUpdatePartial:

    @pytest.fixture()
    def movie(
        self,
        request: SubRequest,
    ) -> Generator[Movies]:
        description = request.param
        movie = create_movie_random_slug(description)
        yield movie
        movie_storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                "some description",
                "other description",
                id="some-description-no-to-description",
            ),
            pytest.param(
                "other description",
                "some description",
                id="no-description-some-to-description",
            ),
            pytest.param(
                "x" * 5,
                "x" * DESCRIPTION_MAX_LENGTH,
                id="min-description-to-max-description",
            ),
            pytest.param(
                "x" * DESCRIPTION_MAX_LENGTH,
                "x" * 5,
                id="max-description-to-min-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self,
        movie: Movies,
        new_description: DescriptionString,
        auth_client: TestClient,
    ) -> None:

        url = app.url_path_for("update_movie_detail_partial", slug=movie.slug)
        response = auth_client.patch(url=url, json={"description": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_in_db = movie_storage.get_by_slug(movie.slug)
        assert movie_in_db.description == new_description, response.text  # type: ignore
