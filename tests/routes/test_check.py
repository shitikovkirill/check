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

    async def test_create_check_with_decimal_quantity(self, client, token):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 1.50, "quantity": 0.5}],
                "payment": {"type": "cache", "amount": 4.5},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("id")
        assert response.json().get("total") == 0.75
        assert response.json().get("rest") == 3.75
        assert response.status_code == 200

    async def test_create_check_with_decimal_quantity_with_round_down(
        self, client, token
    ):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 64.44, "quantity": 0.05}],
                "payment": {"type": "cache", "amount": 4},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("id")
        assert response.json().get("total") == 3.22
        assert response.json().get("rest") == 0.78
        assert response.status_code == 200

    async def test_create_check_with_decimal_quantity_with_round_up(
        self, client, token
    ):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 65.33, "quantity": 0.05}],
                "payment": {"type": "cache", "amount": 4},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("id")
        assert response.json().get("total") == 3.27
        assert response.json().get("rest") == 0.73
        assert response.status_code == 200

    async def test_create_check_with_decimal_quantity_with_round_when_quantity_and_price_very_smol(
        self, client, token
    ):

        response = client.post(
            "/api/check",
            json={
                "products": [{"name": "string", "price": 0.01, "quantity": 0.001}],
                "payment": {"type": "cache", "amount": 4.5},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        assert response.json().get("id")
        assert response.json().get("total") == 0.01
        assert response.json().get("rest") == 4.49
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
