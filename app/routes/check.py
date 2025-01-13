from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import PositiveInt

from app.auth.services.auth import get_current_active_user
from app.check.dependencies import CheckService
from app.check.dto import Check, CheckResponse
from app.check.exceptions import CheckNotFound, NotEnoughPaidMoneyException
from app.check.typs import PaymentTyps
from app.check.validators import PriceDecimalToInt
from app.db.models.user import User

router = APIRouter(
    prefix="/check",
    tags=["checks"],
)


@router.post(
    "",
    response_model=CheckResponse,
    responses={
        status.HTTP_402_PAYMENT_REQUIRED: {
            "description": NotEnoughPaidMoneyException.__doc__,
        }
    },
)
async def create_check(
    check: Check,
    service: CheckService,
    current_user: User = Depends(get_current_active_user),
):
    try:
        result = await service.create(check, current_user)
    except NotEnoughPaidMoneyException as exc:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=str(exc),
        )
    return result


@router.get("", response_model=List[CheckResponse])
async def filter_checks(
    service: CheckService,
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    payment_type: PaymentTyps | None = Query(default=None),
    total_more: PriceDecimalToInt | None = Query(default=None),
    limit: PositiveInt = Query(default=100, gt=0, le=1000),
    offset: PositiveInt = Query(default=0),
    current_user: User = Depends(get_current_active_user),
):
    if start and end and start < end:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Start datetime can not be less then end datetime",
        )
    result = await service.filter(
        current_user, start, end, total_more, payment_type, limit, offset
    )
    return result


@router.get("/{id}", response_model=CheckResponse)
async def get_check(
    id: PositiveInt,
    service: CheckService,
    current_user: User = Depends(get_current_active_user),
):
    try:
        result = await service.get(id, current_user)
    except CheckNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return result
