from pydantic import condecimal

PriceField = condecimal(gt=0, decimal_places=2)
