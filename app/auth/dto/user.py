from pydantic import EmailStr
from sqlmodel import SQLModel

from app.auth.validators import PasswordField


class UserCreate(SQLModel):

    name: str
    email: EmailStr
    password: PasswordField


class UserAuth(SQLModel):

    email: EmailStr
    password: PasswordField
