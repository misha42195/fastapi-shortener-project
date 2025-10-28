from typing import Any

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from dependencies.movies import GetMovieStorage
from templating import templates

router = APIRouter()


@router.get(
    path="/",
    name="movies:list",
    response_class=HTMLResponse,
)
def list_movies(
    request: Request,
    storage: GetMovieStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    movies_list = storage.get_movies()
    context.update(movies_list=movies_list)
    return templates.TemplateResponse(
        request=request,
        name="movies/list.html",
        context=context,
    )
