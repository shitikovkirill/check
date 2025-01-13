class TestCheck:

    async def test_create_check(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 1, "quantity": 1}],
                "payment": {"type": "cache", "amount": 1},
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("id")
        assert response.status_code == 200

    async def test_not_correct_amount(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 100, "quantity": 1}],
                "payment": {"type": "cache", "amount": 1},
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert "Not enough paid money" in response.json().get("detail")
        assert response.status_code == 402
