from datetime import UTC, datetime
from itertools import chain
from typing import List

from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from app.check.dto import Check as CheckDto
from app.check.exceptions import CheckNotFound, NotEnoughPaidMoneyException
from app.check.typs import PaymentTyps
from app.db.dependencies.db import DbSession
from app.db.models.check import Check, Payment, Product
from app.db.models.user import User


class CheckService:

    def __init__(
        self,
        db: DbSession,
    ):
        self.db = db

    async def get(self, id: int, user: User) -> User:
        query = select(Check).where(Check.id == id, Check.user_id == user.id)
        result = await self.db.execute(query)
        try:
            check = result.unique().one()[0]
        except NoResultFound:
            raise CheckNotFound("Check with this id not found")
        return check

    async def get_by_secret(self, secret):
        query = select(Check, User).join(User).where(Check.sectet == secret)
        result = await self.db.execute(query)
        try:
            check_and_owner = result.unique().one()
        except NoResultFound:
            raise CheckNotFound("Check with this id not found")
        return check_and_owner

    async def filter(
        self,
        user: User,
        start: datetime | None,
        end: datetime | None,
        total_more: int | None,
        payment_type: PaymentTyps | None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Check]:
        query = select(Check).where(Check.user_id == user.id)

        if start:
            query = query.where(Check.created_at <= start)
        if end:
            query = query.where(Check.created_at >= end)
        if total_more:
            query = query.where(Check.total >= total_more)
        if payment_type:
            query = query.where(Payment.type == payment_type)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(limit)

        result = await self.db.execute(query)
        checks = result.unique().all()
        return list(chain.from_iterable(checks))

    async def create(self, check: CheckDto, user: User) -> User:
        payment_obj = Payment.model_validate(check.payment)
        self.db.add(payment_obj)
        await self.db.flush()

        total_price = 0
        for product in check.products:
            total_price += product.price * product.quantity

        check_update = {
            "total": total_price,
            "rest": payment_obj.amount - total_price,
            "payment": payment_obj,
            "user_id": user.id,
            "products": [],
        }
        if check_update["rest"] < 0:
            self.db.rollback()
            raise NotEnoughPaidMoneyException()

        check_obj = Check.model_validate(check, update=check_update)
        self.db.add(check_obj)
        await self.db.flush()

        for product in check.products:
            product_obj = Product.model_validate(
                product, update={"check_id": check_obj.id}
            )
            self.db.add(product_obj)

        await self.db.commit()

        await self.db.refresh(check_obj)

        return check_obj
