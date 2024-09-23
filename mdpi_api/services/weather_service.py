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
        weather = await self.weather_dao.get_current_weather(city_id)
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

    async def update_weather_for_all_cities(self) -> None:
        """
        Update weather data for all distinct cities in the favorite_cities table.

        This method fetches weather from the API for each city and updates the database.
        """
        logger.info("Updating weather data for all cities in favorite_cities table...")

        # Fetch all distinct city IDs from the favorite_cities table
        city_dao = CityDAO(self.session)
        cities = await city_dao.get_all_favorite_cities()

        if not cities:
            logger.info("No favorite cities found to update.")
            return

        # Fetch and update weather data for each city
        for city in cities:
            try:
                if await self.weather_dao.get_current_weather(city.id):
                    logger.info(
                        (
                            f"Weather for current hour already exists "
                            f"for city ID {city.id}."
                        ),
                    )
                else:
                    # Call the weather API
                    logger.info(f"Getting weather for city ID {city.id} from API.")
                    api_result = await self.weather_client.get_weather_for_city(
                        city_name=city.name,
                    )
                    # Update the weather data
                    await self.weather_dao.add_weather(
                        WeatherModel(
                            city_id=city.id,
                            data=MutableDict(api_result or {}),
                        ),
                    )
                    logger.info(
                        (
                            f"Weather data updated for city ID {city.id}, "
                            f"name: {city.name}."
                        ),
                    )
            except Exception as ex:
                logger.error(f"Failed to update weather for city ID {city.id}: {ex}")
