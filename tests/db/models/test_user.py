from app.auth.dto.user import UserCreate
from app.auth.providers.password import PasswordProvider
from app.db.models.user import User


async def test_user(db, email):
    pp = PasswordProvider()
    user_dto = UserCreate(name="test", email=email, password="Qwerty1")
    user = User.model_validate(
        user_dto, update={"password": pp.ge_hash(user_dto.password.get_secret_value())}
    )
    assert type(user) is User
    assert user.password is not None
    db.add(user)
    await db.commit()
    assert user.id is not None
    assert user.created_on is not None
    assert user.updated_on is not None
