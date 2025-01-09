from typing import Annotated

from fastapi import Depends

from app.db.service.user import UserRepository as UserRepositoryClass

UserRepository = Annotated[UserRepositoryClass, Depends()]
