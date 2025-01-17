import pytest

from app.check.typs import PaymentTyps
from app.db.models.check import Check, Payment
from app.db.models.user import User


class TestCreateCheck:

    async def test_create_check(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 1.50, "quantity": 2}],
                "payment": {"type": "cache", "amount": 4.5},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("id")
        assert response.json().get("total") == 3
        assert response.json().get("rest") == 1.5
        assert response.status_code == 200

    async def test_not_correct_token(self, client):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 1, "quantity": 1}],
                "payment": {"type": "cache", "amount": 1},
            },
            headers={
                "Authorization": "Bearer token",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("detail") == "Could not validate credentials"
        assert response.status_code == 401

    async def test_not_correct_amount(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 100, "quantity": 1}],
                "payment": {"type": "cache", "amount": 1},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert "Not enough paid money" in response.json().get("detail")
        assert response.status_code == 402

    async def test_not_correct_price(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 100.678, "quantity": 1}],
                "payment": {"type": "cache", "amount": 1},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert "no more than 2 decimal places" in response.json().get("detail")[0].get(
            "msg"
        )
        assert response.status_code == 422

    async def test_not_correct_payment_type(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 1, "quantity": 1}],
                "payment": {"type": "cache2", "amount": 1},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert "Input should be" in response.json().get("detail")[0].get("msg")
        assert response.status_code == 422


class TestFilterCheck:

    @pytest.fixture
    async def checks(self, db, user):
        checks = []

        user = await db.get(User, user.get("id"))
        payment = Payment(type=PaymentTyps.CACHE, amount=1000)
        db.add(payment)
        await db.flush()
        check = Check(payment=payment, total=1000, rest=50, user=user)
        db.add(check)
        await db.commit()

        checks.append(check)
        return checks

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """

    async def test_filter_by_start(self):
        pass
