from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.auth.validators import HashField
from app.db.models.base import IdField, TimeStamp


class User(IdField, TimeStamp, SQLModel, table=True):

    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: HashField = Field(nullable=False, exclude=True)
    is_active: bool = Field(True, nullable=False)
