from typing import Any, Generic, List, TypeVar, Union

from mdpi_api.localization.translator import Translator
from pydantic import BaseModel, Field, field_validator


class EmptyData(BaseModel):
    """Empty data schema."""


DataT = TypeVar("DataT", bound=BaseModel)


class APIResponse(BaseModel, Generic[DataT]):
    """Generic response schema."""

    message: str
    data: Union[DataT, List[DataT], EmptyData, List[Any]]

    @classmethod
    def create(
        cls,
        data: Union[DataT, List[DataT], EmptyData, List[Any]],
        message: str = "success",
        **kwargs: Any,
    ) -> "APIResponse[DataT]":
        """
        Create a success response.

        :param data: The data to return.
        :param message: The message to return.
        :param kwargs: Additional keyword arguments.
        :return: The response.
        """
        translator = Translator()
        message = translator.t(f"response_messages.{message}", **kwargs) or message
        return cls(message=message, data=data)


class PaginationParams(BaseModel):
    """Pagination parameters schema."""

    limit: int = Field(
        default=10,
        ge=1,
        description="The number of cities to return.",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="The offset to start from.",
    )

    @field_validator("limit", mode="after")
    @classmethod
    def validate_limit(cls, value: int) -> int:
        """
        Validate the limit parameter to ensure it is not greater than 100.

        :param value: The value to validate.
        :return: The validated value.
        """
        return min(value, 100)
