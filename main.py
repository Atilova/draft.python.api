from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status

from src.infra.config import load_config


_config = load_config()
app = FastAPI()


@app.get("/api/health/")
def api_health():
    return JSONResponse(
        content=_config.model_dump(),
        status_code=status.HTTP_200_OK,
    )
