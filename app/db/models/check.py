from typing import List

from pydantic import PositiveInt
from sqlmodel import Field, Relationship, SQLModel

from app.check.typs import PaymentTyps
from app.db.models.base import IdField, TimeStamp


class Product(IdField, SQLModel, table=True):
    name: str
    price: PositiveInt
    quantity: PositiveInt

    check_id: int | None = Field(default=None, foreign_key="check.id")


class Payment(IdField, SQLModel, table=True):
    type: PaymentTyps
    amount: PositiveInt


class Check(IdField, TimeStamp, SQLModel, table=True):
    products: List[Product] = Relationship(back_populates="product")
    payment_id: int | None = Field(default=None, foreign_key="payment.id", unique=True)
    payment: Payment = Relationship(back_populates="payment")
    total: PositiveInt
    rest: PositiveInt
