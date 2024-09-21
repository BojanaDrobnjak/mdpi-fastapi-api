from typing import Any, Generic, List, TypeVar, Union

from mdpi_api.localization.translator import Translator
from pydantic import BaseModel


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
