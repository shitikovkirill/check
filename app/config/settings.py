from pydantic_settings import BaseSettings

from app.config.types.environment import EnvironmentType


class Settings(BaseSettings):
    environment: EnvironmentType = EnvironmentType.PRODUCTION

    @property
    def debug(self):
        return self.environment == EnvironmentType.DEVELOPMENT
