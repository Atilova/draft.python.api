from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette import status

from src.infra.config import load_config


_config = load_config()
app = FastAPI(redirect_slashes=False)
_test_counter = Counter(name="test_count", documentation="Test counter")

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return token


@app.get("/api/v1/config/")
def api_config():
    return JSONResponse(
        content=_config.model_dump(),
        status_code=status.HTTP_200_OK,
    )


@app.get("/health")
def health():
    _test_counter.inc()
    return JSONResponse(
        content=None,
        status_code=status.HTTP_200_OK,
    )


@app.get("/metrics")
def metrics():
    return JSONResponse(
        content={},
        status_code=status.HTTP_200_OK,
    )


@app.get("/metrics/")
def metrics_slash(_: str = Depends(verify_token)):
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
