from typing import Any, Mapping

from fastapi import APIRouter
from pydantic import BaseModel, ValidationError
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


def form_pydantic_errors(
    error: ValidationError,
) -> dict[str, str]:
    return {str(err["loc"][0]): err["msg"] for err in error.errors()}


def create_view_validation_response(
    request: Request,
    errors: dict[str, str] | None = None,
    form_date: BaseModel | Mapping[str, Any] | None = None,
    form_validated: bool = True,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = CreateMovies.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        form_validated=form_validated,
        form_data=form_date,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/create.html",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        context=context,
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
            movie_create = CreateMovies.model_validate(form)
        except ValidationError as e:
            errors = form_pydantic_errors(error=e)
            return create_view_validation_response(
                request=request,
                errors=errors,
                form_date=form,
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
    return create_view_validation_response(
        request=request,
        errors=errors,
        form_date=movie_create,
    )
