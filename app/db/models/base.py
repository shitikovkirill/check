from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime
from sqlmodel import Field


class IdField:
    id: int | None = Field(default=None, primary_key=True, index=True)


class TimeStamp:
    created_at: datetime = Field(func.now(), sa_type=UtcDateTime, exclude=True)
    updated_at: datetime = Field(
        func.now(),
        sa_column_kwargs={"onupdate": func.now()},
        sa_type=UtcDateTime,
        exclude=True,
    )


class SoftDelete:
    deleted: bool = Field(False)
