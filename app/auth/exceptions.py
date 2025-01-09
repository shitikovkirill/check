from app.exceptions import AppException


class UserException(AppException):
    """
    Get sam problem with user
    """


class UserAlreadyExist(UserException):
    """
    User not found
    """


class UserNotFound(UserException):
    """
    User not exist
    """


class NotCorrectAuthentication(UserException):
    """
    Not correct authentication
    """
