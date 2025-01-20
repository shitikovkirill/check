from datetime import datetime
from typing import List

from sqlmodel import SQLModel

from app.check.typs import PaymentTyps
from app.check.validators import (
    PriceDecimalToInt,
    PriceIntToDecimal,
    PriceRestIntToDecimal,
    Quantity,
)
from app.db.models.base import IdField


class Product(SQLModel):
    name: str
    price: PriceDecimalToInt
    quantity: Quantity


class Payment(SQLModel):
    type: PaymentTyps
    amount: PriceDecimalToInt


class Check(SQLModel):
    products: List[Product]
    payment: Payment


class ProductResponse(IdField, SQLModel):
    name: str
    price: PriceIntToDecimal
    quantity: Quantity


class PaymentResponse(IdField, SQLModel):
    type: PaymentTyps
    amount: PriceIntToDecimal


class CheckResponse(IdField, SQLModel):
    products: List[ProductResponse]
    payment: PaymentResponse
    total: PriceIntToDecimal
    rest: PriceRestIntToDecimal
    created_at: datetime
