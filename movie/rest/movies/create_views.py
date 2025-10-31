from typing import Annotated, Any

from fastapi import APIRouter, Form
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.movies import GetMovieStorage
from schemas.muvies import CreateMovies
from storage.movies.exeptions import MovieAlreadyExistsError
from templating import templates

router = APIRouter(
    prefix="/create",
)


@router.get(
    path="/",
    name="movies:create-view",
)
def get_page_create_view(
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = CreateMovies.model_json_schema()
    context.update(model_schema=model_schema)
    return templates.TemplateResponse(
        request=request,
        name="movies/create.html",
        context=context,
    )


@router.post(
    path="/",
    name="movies:create",
    response_model=None,
)
def create_movie(
    request: Request,
    movie_create: Annotated[CreateMovies, Form()],
    storage: GetMovieStorage,
) -> RedirectResponse | HTMLResponse:
    try:
        storage.create_raise_already_exists(movie_in=movie_create)
    except MovieAlreadyExistsError:
        errors = {"slug": f"Movie with slug {movie_create.slug!r} already exist"}
    else:
        return RedirectResponse(
            url=request.url_for("movies:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    context: dict[str, Any] = {}
    model_schema = CreateMovies.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        form_validated=True,
        form_data=movie_create,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/create.html",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        context=context,
    )
