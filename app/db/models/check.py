import secrets
from typing import List

from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy import Index
from sqlmodel import Field, Relationship, SQLModel

from app.check.typs import PaymentTyps
from app.db.models.base import IdField, TimeStamp
from app.db.models.user import User


class Product(IdField, SQLModel, table=True):
    name: str
    price: PositiveInt
    quantity: float = Field(gt=0)

    check_id: int = Field(foreign_key="check.id")
    check: "Check" = Relationship(back_populates="products")


class Payment(IdField, SQLModel, table=True):
    type: PaymentTyps = Field(index=True)
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
    total: PositiveInt = Field(index=True)
    rest: NonNegativeInt

    sectet: str = Field(
        default_factory=secrets.token_urlsafe, index=True, unique=True, nullable=False
    )

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="checks")

    __table_args__ = (Index("created_at_index", "created_at"),)
