from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.muvies import Movies
from storage.movies.crud import movie_storage


def test_delete(
    movie: Movies,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)
    response = auth_client.delete(url=url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not movie_storage.exists(movie.slug)
