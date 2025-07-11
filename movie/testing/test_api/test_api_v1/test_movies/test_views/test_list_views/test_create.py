import random
import string
from datetime import date

from starlette import status
from starlette.testclient import TestClient

from main import app
from schemas.muvies import CreateMovies, Movie


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    data: dict[str, str] = CreateMovies(
        title="test_title",
        description="test description",
        release_year=date(2025, 10, 10),
        director="test director",
        slug="".join(random.choices(string.ascii_lowercase, k=10)),
    ).model_dump(mode="json")
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
    print(response.json()["detail"])
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    assert (
        f"Movie with slug='{movie.slug}' already exists." == response.json()["detail"]
    )
