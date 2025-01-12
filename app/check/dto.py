from typing import Annotated, List

from pydantic import AfterValidator, BeforeValidator, PositiveInt
from sqlmodel import SQLModel

from app.check.typs import PaymentTyps
from app.check.validators import PriceField
from app.db.models.base import IdField


class Product(SQLModel):
    name: str
    price: Annotated[PriceField, AfterValidator(lambda v: v * 100)]
    quantity: PositiveInt


class Payment(SQLModel):
    type: PaymentTyps
    amount: Annotated[PriceField, AfterValidator(lambda v: v * 100)]


class Check(SQLModel):
    products: List[Product]
    payment: Payment


class ProductResponse(IdField, SQLModel):
    name: str
    price: Annotated[PriceField, BeforeValidator(lambda v: v / 100)]
    quantity: PositiveInt


class PaymentResponse(IdField, SQLModel):
    type: PaymentTyps
    amount: Annotated[PriceField, BeforeValidator(lambda v: v / 100)]


class CheckResponse(IdField, SQLModel):
    products: List[ProductResponse]
    payment: PaymentResponse
