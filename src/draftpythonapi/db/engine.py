from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.pool import NullPool

from src.draftpythonapi.db.config import DatabaseConfig


def db_engine_factory(config: DatabaseConfig):
    async def _dispose(engine: AsyncEngine):
        await engine.dispose()

    if config.pool.enabled:
        pool_kwargs = {
            "pool_size": config.pool.size,
            "max_overflow": config.pool.max_overflow,
            "pool_timeout": config.pool.timeout,
            "pool_recycle": config.pool.conn_recycle_seconds,
            "pool_pre_ping": config.pool.pre_ping,
        }
    else:
        pool_kwargs = {
            "poolclass": NullPool,
        }

    engine = create_async_engine(
        config.url,
        future=True,
        **pool_kwargs
    )

    yield engine
    yield _dispose(engine)


def get_db_sessionmaker_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    return session_factory
