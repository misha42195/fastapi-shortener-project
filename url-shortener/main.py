from fastapi import (
    FastAPI,
    Request,
)


app = FastAPI(title="URL Shortener")


@app.get("/")
def get_root(request: Request, name: str = "World"):
    docs_path = str(
        request.url.replace(
            path="/docs",
            query="",
        )
    )

    return {"message": f"Hello {name}", "docs_path": docs_path}
