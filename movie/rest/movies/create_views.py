from typing import Annotated, Any

from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse

from schemas.muvies import CreateMovies
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
)
def create_movie(
    movie_create: Annotated[
        CreateMovies,
        Form(),
    ],
) -> dict[str, str]:

    return movie_create.model_dump(mode="json")
