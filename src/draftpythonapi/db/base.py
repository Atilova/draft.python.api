import re
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pkgs.time import datetime_utc_now


class BaseModel(DeclarativeBase):
    PASCAL_TO_SNAKE_CASE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        table_name = (
            cls.PASCAL_TO_SNAKE_CASE_PATTERN.sub("_", cls.__name__).lower().removesuffix("_model")
        )

        return table_name


class BaseUUIDModel(BaseModel):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(pg_UUID(as_uuid=True), primary_key=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(
        default=datetime_utc_now,
        nullable=False,
    )
