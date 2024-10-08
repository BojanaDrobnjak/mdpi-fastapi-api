from fastapi import status
from mdpi_api.web.api.exception_handlers import HTTPExceptionResponseModelError


class WeatherAPIError(HTTPExceptionResponseModelError):
    """Exception raised for weather API errors."""

    def __init__(
        self,
        error_code: str = "",
        message: str = "Weather API error",
        detail: str = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
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
