from datetime import datetime
from typing import Optional

from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime
from sqlmodel import Field


class IdField:
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class TimeStamp:
    created_on: datetime = Field(func.now(), sa_type=UtcDateTime, exclude=True)
    updated_on: datetime = Field(
        func.now(),
        sa_column_kwargs={"onupdate": func.now()},
        sa_type=UtcDateTime,
        exclude=True,
    )


class SoftDelete:
    deleted: bool = Field(False)
