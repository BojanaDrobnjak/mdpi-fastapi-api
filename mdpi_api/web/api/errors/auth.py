from fastapi import status
from mdpi_api.web.api.exception_handlers import HTTPExceptionResponseModelError


class JWTError(HTTPExceptionResponseModelError):
    """Exception raised for JWT error."""

    def __init__(
        self,
        error_code: str = "",
        message: str = "JWT error",
        detail: str = "",
        status_code: int = status.HTTP_403_FORBIDDEN,
    ) -> None:
        """
        Initialize JWTError.

        :param error_code: Error code.
        :param message: Error message.
        :param detail: Error detail.
        :param status_code: Error status code.
        """
        self.error_code = error_code
        self.message = message
        self.detail = detail
        self.status_code = status_code
