from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from dependencies.movies import MovieBySlug
from schemas.muvies import UpdateMovies
from services.movies import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)
response_helper = FormResponseHelper(
    model=UpdateMovies,
    template_name="movies/update.html",
)


@router.get(
    path="/",
    name="movie:update-views",
    response_model=None,
)
def get_page_update_view(
    request: Request,
    movie: MovieBySlug,
) -> HTMLResponse:
    form = UpdateMovies(**movie.model_dump())
    return response_helper.render(
        request=request,
        form_data=form,
        movie=movie,  # type: ignore
    )
