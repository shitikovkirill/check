from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings


class TokenConfig(BaseSettings):
    token_expire: timedelta = timedelta(minutes=30)
    refresh_token_expire: timedelta = timedelta(days=7)

    private_key: str = Field(gt=10)
    public_key: str = Field(gt=10)
