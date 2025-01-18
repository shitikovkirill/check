from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import db_config, settings
from app.config.types.environment import EnvironmentType


def get_engine(dsn: str, environment: EnvironmentType) -> AsyncEngine:
    db_props = {"future": True}
    if environment in [EnvironmentType.DEVELOPMENT, EnvironmentType.TEST]:
        db_props.update({"echo": True})
    if environment == EnvironmentType.TEST:
        db_props.update({"poolclass": NullPool})
    engine = create_async_engine(dsn, **db_props)
    return engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine(str(db_config.url), settings.environment)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
