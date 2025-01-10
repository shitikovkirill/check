

class TestSignUp:
    
    async def test_success_sign_up(self, client, email):
        response = client.post(
            "/api/user",
            json={
                "name": "test",
                "email": email,
                "password": "Qwerty123",
            },
        )
        assert response.json()
        assert response.json().get("id")
        assert response.status_code == 200
        
    async def test_sign_up_with_existing_email(self, client, user):
        
        response = client.post(
            "/api/user",
            json={
                "name": "test",
                "email": user.json().get("email"),
                "password": "Qwerty123",
            },
        )
        assert response.json()
        assert "already exist" in response.json().get("detail")
        assert response.status_code == 406
        
    async def test_sign_up_with_not_correct_email(self, client):
        
        response = client.post(
            "/api/user",
            json={
                "name": "test",
                "email": "test",
                "password": "Qwerty123",
            },
        )
        assert response.json()
        assert len(response.json()) == 1
        assert response.json().get('detail')
        assert "email address must have" in response.json().get('detail')[0].get("msg")
        assert response.status_code == 422
        
        
        
    async def test_sign_up_with_not_correct_password(self, client):
        
        response = client.post(
            "/api/user",
            json={
                "name": "test",
                "email": "test@mail.com",
                "password": "test",
            },
        )
        assert response.json()
        assert len(response.json()) == 1
        assert response.json().get('detail')
        assert "your password must contain" in response.json().get('detail')[0].get("msg")
        assert response.status_code == 422


class TestLogin:
    async def test_login_success(self, client, user):
        
        response = client.post(
            "/api/user/auth",
            json={
                "email": user.json().get("email"),
                "password": "Qwerty123",
            },
        )
        assert response.json()
        assert response.json().get('access_token')
        assert response.status_code == 200
        
    async def test_login_with_not_correct_email(self, client, email):
        
        response = client.post(
            "/api/user/auth",
            json={
                "email": email,
                "password": "Qwerty123",
            },
        )
        assert response.json()
        assert "User with email" in response.json().get('detail')
        assert response.status_code == 406
    
    async def test_login_with_not_correct_password(self, client, user):
        
        response = client.post(
            "/api/user/auth",
            json={
                "email": user.json().get("email"),
                "password": "Zwerty123",
            },
        )
        assert response.json()
        assert "Not correct password" in response.json().get('detail')
        assert response.status_code == 406