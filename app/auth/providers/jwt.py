import json
from datetime import UTC, datetime, timedelta
from typing import Optional

from jose import jws
from jose.constants import ALGORITHMS

from app.auth.dto.token import TokenData
from app.config import token_config
from app.db.models.user import User


class JWTProvider:
    def __init__(self):
        self.private_key = str(token_config.private_key)
        self.public_key = str(token_config.public_key)
        self.algorithm = ALGORITHMS.RS256

    def get(self, data: dict, expires_at: Optional[datetime] = None):
        to_encode = data.copy()
        if not expires_at:
            expires_at = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": int(expires_at.timestamp())})
        encoded_jwt = create_token(
            to_encode, private_key=self.private_key, algorithm=self.algorithm
        )
        return encoded_jwt

    def get_token(self, user: User, expires_at: datetime, additional=None):
        if additional is None:
            additional = {}
        return self.get(
            {"sub": str(user.id), **additional},
            expires_at=expires_at,
        )

    def decode(self, token):
        data = decode_token(token, public_key=self.public_key, algorithm=self.algorithm)
        data["exp"] = datetime.fromtimestamp(data["exp"])
        return TokenData(**data)


def decode_token(token, *, public_key, algorithm=ALGORITHMS.RS256):
    return json.loads(jws.verify(token, public_key, algorithm))


def decode_token_without_verification(token, *, algorithm=ALGORITHMS.RS256):
    return json.loads(jws.verify(token, None, algorithm, verify=False))


def create_token(data, *, private_key, algorithm=ALGORITHMS.RS256):
    return jws.sign(data, private_key, algorithm=algorithm)
