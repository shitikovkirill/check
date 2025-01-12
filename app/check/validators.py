from pydantic import condecimal

PriceField = condecimal(gt=0, strict=True, decimal_places=2)
