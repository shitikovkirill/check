from app.auth.dependencies.providers import PasswordProvider
from app.auth.dto.user import UserCreate
from app.db.dependencies.db import DbSession
from app.db.models.user import User


class UserService:

    def __init__(self, db: DbSession, password_provider: PasswordProvider):
        self.db = db
        self.password_provider = password_provider

    async def create_user(self, user_dto: UserCreate):
        hashed_password = self.password_provider.ge_hash(
            user_dto.password.get_secret_value()
        )
        user = User.model_validate(user_dto, update={"password": hashed_password})
        self.db.add(user)
        await self.db.commit()
        return user
