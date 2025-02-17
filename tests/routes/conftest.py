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
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def token(client, user):

    response = client.post(
        "/api/user/auth",
        json={
            "email": user.get("email"),
            "password": "Qwerty123",
        },
    )
    assert response.status_code == 200
    return response.json().get("access_token")
