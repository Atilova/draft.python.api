import asyncio as aio
import logging

from alembic import context
from alembic.operations.ops import MigrationScript
from alembic.runtime.migration import MigrationContext
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

import src.draftpythonapi.logger.config  # noqa: F401
from migrations import models
from src.draftpythonapi.config import load_config


logger = logging.getLogger(__name__)

_db_config = load_config().database
_config = context.config
_target_metadata = models.BaseModel.metadata

_config.set_main_option("sqlalchemy.url", _db_config.url)


def _process_revision_directives(
    context: MigrationContext,
    revision: str,
    directives: list[MigrationScript],
):
    if not getattr(_config.cmd_opts, "autogenerate", False):
        return

    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []
        logger.info("No changes detected, skipping make migrations")


def run_migrations_offline():
    url = _config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=_target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    def _run(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=_target_metadata,
            process_revision_directives=_process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()

    engine = async_engine_from_config(
        _config.get_section(_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with engine.connect() as connection:
        await connection.run_sync(_run)
        
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    aio.run(run_migrations_online())
