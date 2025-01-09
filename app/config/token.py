from datetime import timedelta
from functools import cached_property

from pydantic import AliasChoices, Field, FilePath
from pydantic_settings import BaseSettings


class TokenConfig(BaseSettings):
    token_expire: timedelta = timedelta(minutes=30)

    private_key_path: FilePath = Field(validation_alias=AliasChoices("private_key"))
    public_key_path: FilePath = Field(validation_alias=AliasChoices("public_key"))

    @cached_property
    def private_key(self):
        with open(self.private_key_path) as f:
            return f.read()

    @cached_property
    def public_key(self):
        with open(self.public_key_path) as f:
            return f.read()
