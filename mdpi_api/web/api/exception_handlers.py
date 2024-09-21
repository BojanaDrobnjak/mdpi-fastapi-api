from typing import Optional

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from loguru import logger
from mdpi_api.localization.translator import Translator
from starlette.responses import JSONResponse


class HTTPExceptionResponseModelError(HTTPException):
    """Base exception class."""

    def __init__(
        self,
        error_code: Optional[str] = "",
        message: Optional[str] = "",
        detail: str = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        """
        Initialize BaseException.

        :param error_code: Error code.
        :param message: Error message.
        :param detail: Error detail.
        :param status_code: Error status code.
        """
        self.error_code = error_code
        self.message = message
        self.detail = detail
        self.status_code = status_code


def http_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    """
    A function used to handle HTTP errors.

    :param request: The request.
    :param exception: The exception to be handled.
    :return: The response.
    """
    if isinstance(exception, HTTPExceptionResponseModelError):
        translator = Translator()
        message_t_key = f"response_messages.{exception.error_code}"
        detail_t_key = f"response_details.{exception.error_code}"
        message = translator.t(message_t_key) or exception.message
        detail = translator.t(detail_t_key) or exception.detail
        logger.exception(f"HTTP error occurred. Message: {message}, Detail: {detail}")
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "error_code": exception.error_code,
                "message": message,
                "detail": detail,
            },
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error_code": "", "message": "Internal Server Error", "detail": ""},
    )


def request_validation_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    """
    A function used to handle request validation errors.

    :param request: The request.
    :param exception: The exception to be handled.
    :return: The response.
    """
    if isinstance(exception, RequestValidationError):
        logger.exception(f"Request validation error occurred: {exception.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "",
                "message": "Request validation error",
                "detail": jsonable_encoder(exception.errors()),
            },
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error_code": "", "message": "Internal Server Error", "detail": ""},
    )
