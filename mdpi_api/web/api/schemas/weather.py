from typing import Any, Dict

from pydantic import BaseModel


class WeatherDTO(BaseModel):
    """Data transfer object for weather data."""

    city_id: int
    city_name: str
    data: Dict[str, Any]

    class Config:
        """Pydantic configuration."""

        from_attributes = True
