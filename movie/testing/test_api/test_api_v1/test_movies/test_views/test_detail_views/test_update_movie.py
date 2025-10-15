from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.muvies import Movies
from storage.movies.crud import movie_storage
from testing.conftest import create_movie_random_slug


class TestUpdate:
    @pytest.fixture()
    def movie(
        self,
        request: SubRequest,
    ) -> Generator[Movies]:
        title, description = request.param
        print(request.param)
        movie = create_movie_random_slug(
            description,
            title,
        )
        yield movie
        movie_storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description",
        [
            pytest.param(
                ("a title", "a description"),
                "new a title",
                "new a description",
                id="a-to-new-a",
            ),
            pytest.param(
                ("b title", "b description"),
                "new b title",
                "new b description",
                id="b-to-new-b",
            ),
            pytest.param(
                ("c title", "c description"),
                "new c title",
                "new c description",
                id="c-to-new-c",
            ),
            pytest.param(
                ("d title", "d description"),
                "new d title",
                "new d description",
                id="d-to-new-d",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movies,
        auth_client: TestClient,
        new_title: str,
        new_description: str,
    ) -> None:
        url = app.url_path_for(
            "update_movie_details",
            slug=movie.slug,
        )
        data = movie.model_dump(mode="json")
        data["title"] = new_title
        data["description"] = new_description

        response = auth_client.put(
            url=url,
            json=data,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        movie_in_db = movie_storage.get_by_slug(movie.slug)
        if movie_in_db is not None:
            assert movie_in_db.description == new_description
            assert movie_in_db.title == new_title
