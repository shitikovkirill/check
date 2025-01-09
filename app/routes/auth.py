from fastapi import APIRouter

from app.auth.dependencies.services import UserService
from app.auth.dto.user import UserCreate
from app.db.models.user import User

router = APIRouter()


@router.post("/registration/", response_model=User)
async def regisration(user: UserCreate, user_service: UserService):
    user = await user_service.create_user(user)
    return user
