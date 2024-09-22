from fastapi import Depends
from loguru import logger
from mdpi_api.db.dao.city_dao import CityDAO
from mdpi_api.db.dao.weather_dao import WeatherDAO
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.db.models.weather_model import WeatherModel
from mdpi_api.integrations.weather_client import WeatherAPIClient
from mdpi_api.web.api.errors.city import CityNotFoundError
from mdpi_api.web.api.schemas.weather import WeatherDTO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.mutable import MutableDict


class WeatherService:
    """Class for city service."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.weather_dao = WeatherDAO(session)
        self.weather_client = WeatherAPIClient()

    async def get_weather_by_city_id(self, city_id: int) -> WeatherDTO:
        """
        Get weather data for a city by city ID.

        :param city_id: The ID of the city.
        :return: WeatherDTO.

        :raises CityNotFoundError: If the city is not found.
        """
        weather = await self.weather_dao.get_weather_by_city_id(city_id)
        if not weather:
            # Call the weather API
            logger.info(f"Getting weather for city ID {city_id} from API.")
            city_dao = CityDAO(self.session)
            city = await city_dao.get_by_id(city_id)
            if not city:
                raise CityNotFoundError(detail=f"City with ID {city_id} not found.")
            api_result = await self.weather_client.get_weather_for_city(
                city_name=city.name,
            )
            # Save the weather data, TODO: add this to a task queue
            await self.weather_dao.add_weather(
                WeatherModel(
                    city_id=city_id,
                    data=MutableDict(api_result or {}),
                ),
            )
            return api_result
        return WeatherDTO(**weather)
