import re
from typing import Annotated

from pydantic import AfterValidator, SecretStr


class PasswordFieldValidator:
    """
    Password field
    """

    pattern = re.compile(
        r"^.*(?=.{6,})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*#()_+={}?:~\[\]]+$"
    )

    @classmethod
    def validate(cls, value: SecretStr):
        if not isinstance(value, SecretStr):
            raise TypeError("SecretStr required")
        v = value.get_secret_value()
        m = cls.pattern.fullmatch(v)
        if not m:
            raise ValueError(
                "your password must contain "
                "at last one capitalised lower letter "
                "and digit"
            )
        return value


class HashFieldValidator:
    """
    Password field
    """

    pattern = re.compile(r"^\$2[ayb]\$.{56}$")

    @classmethod
    def validate(cls, value: str):
        m = cls.pattern.fullmatch(value)
        if not m:
            raise ValueError("data not hashed")
        return value


PasswordField = Annotated[SecretStr, AfterValidator(PasswordFieldValidator.validate)]

HashField = Annotated[str, AfterValidator(HashFieldValidator.validate)]
