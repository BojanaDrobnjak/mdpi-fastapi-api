from typing import Any, Dict, Optional

from fastapi import Depends
from loguru import logger
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.db.models.city_model import CityModel
from mdpi_api.db.models.weather_model import WeatherModel
from sqlalchemy import and_, join, select
from sqlalchemy.ext.asyncio import AsyncSession


class WeatherDAO:
    """Class for accessing weather table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_weather_by_city_id(self, city_id: int) -> Optional[Dict[str, Any]]:
        """
        Get weather data for a city by city ID.

        :param city_id: The ID of the city.
        :return: Weather model if found, None otherwise.

        :raises Exception: If there is an error during weather retrieval.
        """
        try:
            stmt = (
                select(
                    WeatherModel.id,
                    WeatherModel.city_id,
                    CityModel.name.label("city_name"),
                    WeatherModel.data,
                )
                .select_from(
                    join(WeatherModel, CityModel, WeatherModel.city_id == CityModel.id),
                )
                .where(and_(WeatherModel.city_id == city_id))
            )

            result = await self.session.execute(stmt)
            row = result.first()

            if row:
                weather_data = {
                    "city_id": row.city_id,
                    "city_name": row.city_name,
                    "data": row.data,
                }
                logger.info(f"Got weather by city ID {city_id}: {weather_data}")
                return weather_data
            return None
        except Exception as exception:
            logger.error(f"Failed to get weather by city ID: {exception}")
            raise exception

    async def add_weather(self, weather: WeatherModel) -> None:
        """
        Insert weather data.

        :param weather: The weather model.

        :raises Exception: If there is an error during weather insertion.
        """
        try:
            self.session.add(weather)
            await self.session.flush()
            await self.session.refresh(weather)
            logger.info(f"Inserted weather: {weather}")
        except Exception as exception:
            await self.session.rollback()
            logger.error(f"Failed to insert weather: {exception}")
            raise exception
