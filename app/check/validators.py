from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, PlainSerializer, condecimal

PriceField = condecimal(gt=0, decimal_places=2)
PriceRestField = condecimal(ge=0, decimal_places=2)
PriceDecimalToInt = Annotated[PriceField, AfterValidator(lambda v: v * 100)]
PriceIntToDecimal = Annotated[
    PriceField,
    BeforeValidator(lambda v: v / 100),
    PlainSerializer(lambda x: float(x), return_type=float),
]
PriceRestIntToDecimal = Annotated[
    PriceRestField,
    BeforeValidator(lambda v: v / 100),
    PlainSerializer(lambda x: float(x), return_type=float),
]

Quantity = condecimal(gt=0, decimal_places=3)
