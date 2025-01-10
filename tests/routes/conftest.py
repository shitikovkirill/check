import pytest
from fastapi.testclient import TestClient

from app.__main__ import app


@pytest.fixture(scope="session")
def client():
    # app.dependency_overrides[get_captcha] = get_captcha_mock
    return TestClient(app)


@pytest.fixture
async def user(client, email):
    response = client.post(
        "/api/user",
        json={
            "name": "test",
            "email": email,
            "password": "Qwerty123",
        },
    )
    return response
