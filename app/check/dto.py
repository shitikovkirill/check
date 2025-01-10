from typing import List

from pydantic import PositiveInt
from sqlmodel import SQLModel

from app.check.typs import PaymentTyps
from app.check.validators import PriceField


class Product(SQLModel):
    name: str
    price: PriceField
    quantity: PositiveInt


class Payment(SQLModel):
    type: PaymentTyps
    amount: PriceField


class Check(SQLModel):
    products: List[Product]
    payment: Payment
