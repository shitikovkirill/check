from fastapi import APIRouter, Depends

from app.auth.services.auth import get_current_active_user
from app.check.dependencies import CheckService
from app.check.dto import Check, CheckResponse
from app.db.models.user import User

router = APIRouter(
    prefix="/check",
    tags=["checks"],
)


@router.post("", response_model=CheckResponse)
async def create_check(
    check: Check,
    service: CheckService,
    current_user: User = Depends(get_current_active_user),
):
    result = await service.create(check, current_user)
    return result
