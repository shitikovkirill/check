from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.dependencies.providers import JWTProvider
from app.auth.exceptions import InvalidTockenException
from app.db.dependencies.db import DbSession
from app.db.models.user import User

security = HTTPBearer()


async def get_current_user(
    db: DbSession,
    jwt_provider: JWTProvider,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    _, token = credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authenticate": "Bearer"},
    )
    try:
        payload = jwt_provider.decode(token[1])
        if payload.id is None:
            raise credentials_exception
    except InvalidTockenException:
        raise credentials_exception
    user = await db.get(User, int(payload.id))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
