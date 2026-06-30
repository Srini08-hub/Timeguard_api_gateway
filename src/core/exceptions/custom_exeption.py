from src.core.exceptions.base_exception import GatewayException


class UnauthorizedException(GatewayException):
    """Raised when user is not authenticated (missing or invalid credentials)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=401)


class ForbiddenException(GatewayException):
    """Raised when user is authenticated but not authorized to perform an action."""

    def __init__(self, message: str):
        super().__init__(message, status_code=403)
