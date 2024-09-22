from typing import Any, Dict

import httpx
import polars as pl
from fastapi import status
from loguru import logger
from mdpi_api.settings import Settings
from mdpi_api.web.api.errors.weather import WeatherAPIError
from mdpi_api.web.api.schemas.weather import WeatherDTO

weather_api = Settings().weather_api

KELVIN_TO_CELSIUS = 273.15


class WeatherAPIClient:
    """Client for interacting with the weather API."""

    def __init__(self) -> None:
        self.base_url = weather_api.base_url
        self.api_key = weather_api.api_key

    async def get_weather_for_city(self, *, city_name: str) -> WeatherDTO:
        """
        Fetch weather data for a city by its name.

        :param city_name: The name of the city.
        :return: WeatherDTO if found, None otherwise.

        :raises WeatherAPIError: If there is an error during weather retrieval.
        """
        url = f"{self.base_url}?q={city_name}&appid={self.api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                return self._manipulate_data(data)
            logger.error(f"Failed to fetch weather for {city_name}: {response.text}")
            raise WeatherAPIError(detail="Failed to fetch weather data.")

    @staticmethod
    def _manipulate_data(data: Dict[str, Any]) -> WeatherDTO:
        """
        Manipulate the data from the weather API.

        :param data: The weather data.
        :return: Manipulated weather data.
        """
        main_data = data.pop("main", {})
        df_main = pl.DataFrame([main_data])
        # Convert temperature from Kelvin to Celsius
        df_main = df_main.with_columns(
            [
                (pl.col("temp") - KELVIN_TO_CELSIUS).round(0).alias("temp"),
                (pl.col("temp_min") - KELVIN_TO_CELSIUS).round(0).alias("temp_min"),
                (pl.col("temp_max") - KELVIN_TO_CELSIUS).round(0).alias("temp_max"),
                (pl.col("feels_like") - KELVIN_TO_CELSIUS).round(0).alias("feels_like"),
            ],
        )
        df_other = pl.DataFrame([data])
        # Combine the two dataframes
        df = df_other.hstack(df_main)

        manipulated_data = {col: df[col].to_list()[0] for col in df.columns}
        logger.info(f"Manipulated weather data: {manipulated_data}")

        return WeatherDTO(
            city_id=manipulated_data["id"],
            city_name=manipulated_data["name"],
            data=manipulated_data,
        )
