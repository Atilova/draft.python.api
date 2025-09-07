from uuid import UUID

from sqlalchemy import String, select, exists
from sqlalchemy.dialects.postgresql import (
    ARRAY as pg_ARRAY,
    JSONB as pg_JSONB,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from src.draftpythonapi.db import BaseUUIDModel
from src.identity.domain import IdentityKey


class IdentityKeyModel(BaseUUIDModel):
    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )
    public_jwk: Mapped[dict] = mapped_column(
        pg_JSONB,
        nullable=False,
    )
    permissions: Mapped[list[str]] = mapped_column(
        pg_ARRAY(String),
        nullable=False,
        default=list,
    )


class IdentityRepository:
    __slots__ = (
        "_session",
    )

    def __init__(self, session: AsyncSession):
        self._session = session

    async def exists(self, name: str) -> bool:
        stmt = select(exists().where(IdentityKeyModel.name == name))
        result = await self._session.execute(stmt)
        does_exist = result.scalars()

        return does_exist

    async def save[PublicKey](self, identity_key: IdentityKey[PublicKey]): ...

    async def get[PublicKey](self, key_id: UUID) -> IdentityKey[PublicKey]: ...
