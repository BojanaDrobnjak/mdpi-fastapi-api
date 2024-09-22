from typing import Optional

from fastapi import Depends
from loguru import logger
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.db.models.weather_model import WeatherModel
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class WeatherDAO:
    """Class for accessing weather table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_weather_by_city_id(self, city_id: int) -> Optional[WeatherModel]:
        """
        Get weather data for a city by city ID.

        :param city_id: The ID of the city.
        :return: Weather model if found, None otherwise.

        :raises Exception: If there is an error during weather retrieval.
        """
        try:
            stmt = select(WeatherModel).where(and_(WeatherModel.city_id == city_id))
            result = await self.session.execute(stmt)
            weather = result.scalars().first()
            logger.info(f"Got weather by city ID {city_id}: {weather}")
            return weather
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
