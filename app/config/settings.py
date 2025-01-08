# mypy: ignore-errors
from typing import Set

from pydantic import HttpUrl
from pydantic_settings import BaseSettings

from app.config.types.environment import EnvironmentType


class Settings(BaseSettings):
    environment: EnvironmentType = EnvironmentType.PRODUCTION

    @property
    def debug(self):
        return self.environment == EnvironmentType.DEVELOPMENT
