import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class JwtToken(BaseModel):
    access_token: str
    expires_in: datetime
    token_type: str = "Bearer"


class TokenData(BaseModel):
    id: Optional[uuid.UUID] = Field(None, alias="sub")
