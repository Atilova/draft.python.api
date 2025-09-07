from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from src.draftpythonapi.config import load_config
from src.draftpythonapi.exceptions import BusinessError
from src.identity.api import router


_config = load_config()
app = FastAPI()
app.include_router(router)


@app.exception_handler(BusinessError)
async def handle_business_error(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message}
    )


@app.get("/api/health/")
def api_health():
    return JSONResponse(
        content=_config.model_dump(),
        status_code=status.HTTP_200_OK,
    )
