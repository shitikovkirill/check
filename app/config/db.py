# mypy: ignore-errors
from functools import cached_property

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    user: str = "postgres"
    password: str = "password"
    name: str = "postgres"
    host: str = "localhot"
    port: int = 5432

    @cached_property
    def url(self):
        dns = PostgresDsn(
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )
        return str(dns)
