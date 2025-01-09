from datetime import UTC, datetime

from sqlmodel import select

from app.auth.dependencies.providers import JWTProvider, PasswordProvider
from app.auth.dto.token import JwtToken
from app.auth.dto.user import UserAuth, UserCreate
from app.auth.exceptions import NotCorrectAuthentication, UserNotFound
from app.config import token_config
from app.db.dependencies.db import DbSession
from app.db.models.user import User


class UserService:

    def __init__(
        self,
        db: DbSession,
        password_provider: PasswordProvider,
        jwt_provider: JWTProvider,
    ):
        self.db = db
        self.password_provider = password_provider
        self.jwt_provider = jwt_provider

    async def create_user(self, user_dto: UserCreate) -> User:
        hashed_password = self.password_provider.ge_hash(
            user_dto.password.get_secret_value()
        )
        user = User.model_validate(user_dto, update={"password": hashed_password})
        self.db.add(user)
        await self.db.commit()
        return user

    async def autentificate(self, user_dto: UserAuth) -> User:
        query = select(User).where(User.email == user_dto.email)
        result = await self.db.execute(query)
        user = result.scalar()

        if not user:
            raise UserNotFound()

        if self.password_provider.verify(
            user_dto.password.get_secret_value(), user.password
        ):
            return user
        raise NotCorrectAuthentication()

    async def generate_jwt(self, user: User) -> JwtToken:
        expires_at = datetime.now(UTC) + token_config.token_expire
        token = self.jwt_provider.get_token(user, expires_at)
        return JwtToken(access_token=token, expires_in=expires_at)
