from fastapi import (
    FastAPI,
)
from starlette.requests import Request
from api import router as api_router
from api.redirect_views import router as redirect_router

app = FastAPI(title="Movies")
app.include_router(api_router)
app.include_router(redirect_router)


@app.get("/")
def get_root(request: Request, name: str = "World"):
    docs_path = str(
        request.url.replace(
            path="/docs",
            query="",
        )
    )

    return {
        "message": f"Hello {name}",
        "docs_path": docs_path,
    }
