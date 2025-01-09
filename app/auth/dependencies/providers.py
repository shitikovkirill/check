from typing import Annotated

from fastapi import Depends

# from app.auth.providers.jwt import JWTProvider as JWTProviderClass
from app.auth.providers.password import PasswordProvider as PasswordProviderClass

# JWTProvider = Annotated[JWTProviderClass, Depends()]
PasswordProvider = Annotated[PasswordProviderClass, Depends()]
