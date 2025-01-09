from typing import Annotated

from fastapi import Depends

from app.auth.services.user import UserService as UserServiceClass

UserService = Annotated[UserServiceClass, Depends()]
