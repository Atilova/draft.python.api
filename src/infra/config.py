from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GunicornConfig(BaseModel):
    bind: str = "0.0.0.0:8000"
    workers: int = 1
    threads: int = 8
    worker_class: Literal["uvicorn.workers.UvicornWorker"] = Field(
        alias="workerClass", default="uvicorn.workers.UvicornWorker"
    )
    loglevel: str = "info"
    timeout: int = 60
    access_logs: bool = Field(alias="accessLogs", default=False)


class DatabaseConfig(BaseModel):
    class _Pool(BaseModel):
        size: int = 1
        conn_recycle_seconds: int = Field(alias="connRecycleSeconds", default=600)

    username: str = "draft.python.api"
    password: str = "draft.python.api"  # noqa: S105
    pool: _Pool = Field(default_factory=_Pool)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="cf__",
        env_nested_delimiter="__",
    )

    gunicorn: GunicornConfig = Field(default_factory=GunicornConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)


def load_config() -> Config:
    return Config()
