from app.check.dto import Check as CheckDto
from app.db.dependencies.db import DbSession
from app.db.models.check import Check, Payment, Product
from app.db.models.user import User


class CheckService:

    def __init__(
        self,
        db: DbSession,
    ):
        self.db = db

    async def create(self, check: CheckDto, user: User):
        payment_obj = Payment.model_validate(check.payment)
        self.db.add(payment_obj)
        await self.db.commit()

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
