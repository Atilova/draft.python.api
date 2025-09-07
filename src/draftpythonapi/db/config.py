from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    class _Pool(BaseModel):
        enabled: bool = False
        size: int = 5
        max_overflow: int = Field(alias="maxOverflow", default=10)
        timeout: int = 30
        conn_recycle_seconds: int = Field(alias="connRecycleSeconds", default=600)
        pre_ping: bool = Field(alias="prePing", default=True)

    host: int = "localhost"
    port: int = 5432
    name: str = "draftpythonapi"
    username: str = "draftpythonapi"
    password: str = "draftpythonapi"  # noqa: S105
    pool: _Pool = Field(default_factory=_Pool)

    @property
    def url(self):
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )
