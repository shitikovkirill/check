from fastapi import APIRouter

from app.auth.dependencies.services import UserService
from app.auth.dto.token import JwtToken
from app.auth.dto.user import UserAuth, UserCreate
from app.db.models.user import User

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post("", response_model=User)
async def regisration(user: UserCreate, user_service: UserService):
    user = await user_service.create_user(user)
    return user


@router.post("/auth", response_model=JwtToken)
async def autorisation(user: UserAuth, user_service: UserService):
    user = await user_service.autentificate(user)
    jwt = await user_service.generate_jwt(user)
    return jwt
