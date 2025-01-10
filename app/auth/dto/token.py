import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class JwtToken(BaseModel):
    access_token: str
    expires_in: datetime
    token_type: str = "Bearer"


class TokenData(BaseModel):
    id: uuid.UUID | None = Field(None, alias="sub")
