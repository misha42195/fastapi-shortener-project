from fastapi import (
    APIRouter,
    Request,
)
from pydantic import ValidationError
from starlette import status
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
)

from dependencies.movies import (
    GetMovieStorage,
    MovieBySlug,
)
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
        movie=movie,
    )


@router.post(
    path="/",
    name="movie:update",
    response_model=None,
)
async def update_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMovieStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            movie_update = UpdateMovies.model_validate(
                form,
            )
        except ValidationError as e:
            return response_helper.render(
                request=request,
                pydantic_error=e,
                form_data=form,
                form_validated=True,
                movie=movie,
            )

    storage.update_movie(
        movie=movie,
        movie_in=movie_update,
    )
    return RedirectResponse(
        url=request.url_for(
            "movies:list",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )
