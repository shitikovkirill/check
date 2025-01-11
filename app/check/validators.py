import re
from decimal import Decimal
from typing import Annotated

import annotated_types


class PriceValidator:
    """
    Password field
    """

    pattern = re.compile(r"^\d(\.\d{1,2})?$")

    @classmethod
    def validate(cls, value: Decimal):
        m = cls.pattern.fullmatch(str(value))
        if not m:
            raise ValueError(
                "Not correct price format:" " the decimal part must not exceed 2 digits"
            )
        return value


PriceField = Annotated[Decimal, annotated_types.Interval(gt=0), PriceValidator.validate]
