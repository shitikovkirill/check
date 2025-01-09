from passlib.context import CryptContext


class PasswordProvider:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def ge_hash(self, password: str) -> str:
        return self.context.hash(password)
