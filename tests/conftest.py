import pytest

from app.db.connect import get_session


@pytest.fixture
async def db():
    Session = get_session()

    async for session in Session:
        yield session
