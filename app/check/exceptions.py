from app.exceptions import AppException


class CheckException(AppException):
    """
    Get sam problem with user
    """


class CheckNotFound(CheckException):
    """
    Check not found
    """


class NotEnoughPaidMoneyException(CheckException):
    """
    Not enough paid money
    """
