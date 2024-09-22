import uuid
from typing import List

from fastapi import Depends
from loguru import logger
from mdpi_api.db.dao.city_dao import CityDAO
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.web.api.errors.city import CityNotFoundError
from mdpi_api.web.api.schemas.city import CityDTO, FavoriteCityDTO
from mdpi_api.web.api.schemas.common import PaginationParams
from sqlalchemy.ext.asyncio import AsyncSession


class CityService:
    """Class for city service."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.city_dao = CityDAO(session)

    async def get_all_cities(self, pagination: PaginationParams) -> List[CityDTO]:
        """
        Get all cities.

        :param pagination: The pagination parameters.
        :return: List of cities.

        :raises Exception: If there is an error during city retrieval.
        """
        try:
            cities = await self.city_dao.get_all(
                limit=pagination.limit,
                offset=pagination.offset,
            )
            return [CityDTO.from_orm(city) for city in cities]
        except Exception as exception:
            logger.error(f"Failed to get cities: {exception}")
            raise exception

    async def get_favorite_cities(self, user_id: str) -> List[FavoriteCityDTO]:
        """
        Get all favorite cities for a user.

        :param user_id: ID of the user.
        :return: List of favorite cities.

        :raises Exception: If there is an error during city retrieval.
        """
        try:
            cities = await self.city_dao.get_favorite_cities(uuid.UUID(user_id))
            return [FavoriteCityDTO.from_orm(city) for city in cities]
        except Exception as exception:
            logger.error(f"Failed to get favorite cities: {exception}")
            raise exception

    async def add_favorite_city(self, user_id: str, city_id: int) -> None:
        """
        Add a city to the user's list of favorite cities.

        :param user_id: ID of the user.
        :param city_id: ID of the city.

        :raises CityNotFoundError: If the city is not found.
        :raises Exception: If there is an error during city addition.
        """
        try:
            if await self.city_dao.get_by_id(city_id) is None:
                raise CityNotFoundError(detail=f"City with ID {city_id} not found.")
            await self.city_dao.add_favorite_city(uuid.UUID(user_id), city_id)
        except Exception as exception:
            logger.error(f"Failed to add favorite city: {exception}")
            raise exception

    async def remove_favorite_city(self, user_id: str, city_id: int) -> None:
        """
        Remove a city from the user's list of favorite cities.

        :param user_id: ID of the user.
        :param city_id: ID of the city.

        :raises Exception: If there is an error during city removal.
        """
        try:
            await self.city_dao.remove_favorite_city(uuid.UUID(user_id), city_id)
        except Exception as exception:
            logger.error(f"Failed to remove favorite city: {exception}")
            raise exception

    async def toggle_notifications(self, user_id: str, city_id: int) -> None:
        """
        Toggle notifications for a city.

        :param user_id: ID of the user.
        :param city_id: ID of the city.

        :raises Exception: If there is an error during notifications toggle.
        """
        try:
            await self.city_dao.toggle_notifications(uuid.UUID(user_id), city_id)
        except Exception as exception:
            logger.error(f"Failed to toggle notifications: {exception}")
            raise exception
