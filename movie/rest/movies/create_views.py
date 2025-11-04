from fastapi import APIRouter
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
)

from dependencies.movies import GetMovieStorage
from schemas.muvies import CreateMovies
from services.movies import FormResponseHelper
from storage.movies.exeptions import MovieAlreadyExistsError

router = APIRouter(
    prefix="/create",
)

response_helper = FormResponseHelper(
    model=CreateMovies,
    template_name="movies/create.html",
)


@router.get(
    path="/",
    name="movies:create-view",
)
def get_page_create_view(
    request: Request,
) -> HTMLResponse:
    return response_helper.create_view_validation_response(
        request=request,
    )


@router.post(
    path="/",
    name="movies:create",
    response_model=None,
)
async def create_movie(
    request: Request,
    storage: GetMovieStorage,
) -> RedirectResponse | HTMLResponse:

    async with request.form() as form:
        try:
            movie_create = CreateMovies.model_validate(
                form,
            )
        except ValidationError as e:
            return response_helper.create_view_validation_response(
                request=request,
                pydantic_error=e,
                form_data=form,
                form_validated=True,
            )

    try:
        storage.create_raise_already_exists(movie_in=movie_create)
    except MovieAlreadyExistsError:
        errors = {"slug": f"Movie with slug {movie_create.slug!r} already exist"}
    else:
        return RedirectResponse(
            url=request.url_for("movies:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return response_helper.create_view_validation_response(
        request=request,
        errors=errors,
        form_data=movie_create,
        form_validated=True,
    )
