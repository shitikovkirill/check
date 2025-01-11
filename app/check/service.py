from app.check.dto import Check as CheckDto
from app.db.dependencies.db import DbSession
from app.db.models.check import Check, Payment
from app.db.models.user import User


class CheckService:

    def __init__(
        self,
        db: DbSession,
    ):
        self.db = db

    async def create(self, check: CheckDto, user: User):
        payment = Payment.model_validate(
            check.payment, update={"amount": check.payment.amount * 100}
        )
        # await self.db.commit(payment)
        # total_price = 0
        # for product in check.products:
        #    total_price += product.price * product.quantity
        # check_db = Check.model_validate(check, update={"password": hashed_password})
        return payment
