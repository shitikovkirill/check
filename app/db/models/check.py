from typing import List

from pydantic import NonNegativeInt, PositiveInt
from sqlmodel import Field, Relationship, SQLModel

from app.check.typs import PaymentTyps
from app.db.models.base import IdField, TimeStamp


class Product(IdField, SQLModel, table=True):
    name: str
    price: PositiveInt
    quantity: PositiveInt

    check_id: int = Field(foreign_key="check.id")
    check: "Check" = Relationship(back_populates="products")


class Payment(IdField, SQLModel, table=True):
    type: PaymentTyps
    amount: PositiveInt

    check: "Check" = Relationship(back_populates="payment")


class Check(IdField, TimeStamp, SQLModel, table=True):
    products: List[Product] = Relationship(
        back_populates="check", sa_relationship_kwargs={"lazy": "joined"}
    )
    payment_id: int = Field(
        default=None, foreign_key="payment.id", unique=True, nullable=False
    )
    payment: Payment = Relationship(
        back_populates="check", sa_relationship_kwargs={"lazy": "joined"}
    )
    total: PositiveInt
    rest: NonNegativeInt

    user_id: int = Field(foreign_key="user.id")
