from enum import StrEnum, auto


class EnvironmentType(StrEnum):
    PRODUCTION = "prod"
    DEVELOPMENT = "dev"
    TEST = auto()
