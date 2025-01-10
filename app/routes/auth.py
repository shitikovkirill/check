from fastapi import APIRouter, HTTPException, status

from app.auth.dependencies.services import UserService
from app.auth.dto.token import JwtToken
from app.auth.dto.user import UserAuth, UserCreate
from app.auth.exceptions import AuthException
from app.db.models.user import User

router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={406: {"description": "User with this email already exist"}},
)


@router.post("", response_model=User)
async def regisration(user: UserCreate, user_service: UserService):
    try:
        user = await user_service.create_user(user)
    except AuthException as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(exc))
    return user


@router.post("/auth", response_model=JwtToken)
async def autorisation(user: UserAuth, user_service: UserService):
    try:
        user = await user_service.autentificate(user)
    except AuthException as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(exc))
    jwt = await user_service.generate_jwt(user)
    return jwt
