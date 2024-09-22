from fastapi import status
from mdpi_api.web.api.exception_handlers import HTTPExceptionResponseModelError


class FavoriteCityNotFoundError(HTTPExceptionResponseModelError):
    """Exception raised for favorite city not found."""

    def __init__(
        self,
        error_code: str = "",
        message: str = "Favorite city not found",
        detail: str = "",
        status_code: int = status.HTTP_404_NOT_FOUND,
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


class CityNotFoundError(HTTPExceptionResponseModelError):
    """Exception raised for city not found."""

    def __init__(
        self,
        error_code: str = "",
        message: str = "City not found",
        detail: str = "",
        status_code: int = status.HTTP_404_NOT_FOUND,
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
