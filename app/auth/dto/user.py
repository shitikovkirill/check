from pydantic import EmailStr, Field
from sqlmodel import SQLModel

from app.auth.validators import PasswordField


class UserCreate(SQLModel):

    name: str
    email: EmailStr
    password: PasswordField = Field(exclude=True)
