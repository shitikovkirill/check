from app.exceptions import AppException


class AuthException(AppException):
    """
    Get sam problem with user
    """


class UserAlreadyExist(AuthException):
    """
    User already exist
    """


class UserNotFound(AuthException):
    """
    User not exist
    """


class NotCorrectAuthentication(AuthException):
    """
    Not correct authentication
    """


class InvalidTockenException(AuthException):
    "Not correct token"
