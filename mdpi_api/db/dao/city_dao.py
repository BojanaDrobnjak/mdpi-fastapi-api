from typing import Any, Dict, List, Optional

from fastapi import Depends
from loguru import logger
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.db.models.city_model import CityModel
from mdpi_api.db.models.favorite_cities_model import FavoriteCityModel
from mdpi_api.web.api.errors.city import (
    FavoriteCityAlreadyExistsError,
    FavoriteCityNotFoundError,
)
from pydantic import UUID4
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class CityDAO:
    """Class for accessing cities table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_by_id(self, city_id: int) -> Optional[CityModel]:
        """
        Get a city by ID.

        :param city_id: The ID of the city.
        :return: City model.

        :raises Exception: If there is an error during city retrieval.
        """
        try:
            result = await self.session.execute(
                select(CityModel).where(and_(CityModel.id == city_id)),
            )
            return result.scalar()
        except Exception as exception:
            logger.error(f"Failed to get city by ID: {exception}")
            raise exception

    async def get_all(self, *, limit: int, offset: int) -> List[CityModel]:
        """
        Get all cities.

        :param limit: The number of cities to return.
        :param offset: The offset to start from.
        :return: True if credentials are verified, False otherwise.

        :raises Exception: If there is an error during city retrieval.
        """
        try:
            result = await self.session.execute(
                select(CityModel).limit(limit).offset(offset),
            )
            cities = result.scalars().all()
            return list(cities)
        except Exception as exception:
            logger.error(f"Failed to get cities: {exception}")
            raise exception

    async def get_favorite_cities(self, user_id: UUID4) -> List[Dict[str, Any]]:
        """
        Get all favorite cities for a user.

        :param user_id: ID of the user.
        :return: List of favorite cities.

        :raises Exception: If there is an error during city retrieval.
        """
        try:
            result = await self.session.execute(
                select(
                    CityModel.id,
                    CityModel.name,
                    FavoriteCityModel.allow_notifications,
                )
                .join(FavoriteCityModel, CityModel.id == FavoriteCityModel.city_id)
                .where(FavoriteCityModel.user_id == user_id),
            )
            cities = result.mappings().all()
            return [dict(city) for city in cities]
        except Exception as exception:
            logger.error(f"Failed to get favorite cities: {exception}")
            raise exception

    async def add_favorite_city(self, user_id: UUID4, city_id: int) -> None:
        """
        Add a city to the user's list of favorite cities.

        :param user_id: ID of the user.
        :param city_id: ID of the city.

        :raises FavoriteCityAlreadyExistsError: If the city already exists in favorites.
        :raises Exception: If there is an error during city addition.
        """
        try:
            stmt = insert(FavoriteCityModel).values(
                user_id=user_id,
                city_id=city_id,
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except IntegrityError as ie:
            logger.error(f"City already exists in favorites: {ie}")
            await self.session.rollback()
            raise FavoriteCityAlreadyExistsError(
                detail=f"City with ID {city_id} already exists in favorites.",
            )
        except Exception as exception:
            logger.error(f"Failed to add favorite city: {exception}")
            raise exception

    async def remove_favorite_city(self, user_id: UUID4, city_id: int) -> None:
        """
        Remove a city from the user's list of favorite cities.

        :param user_id: ID of the user.
        :param city_id: ID of the city.

        :raises Exception: If there is an error during city removal.
        """
        try:
            stmt = delete(FavoriteCityModel).where(
                and_(
                    FavoriteCityModel.user_id == user_id,
                    FavoriteCityModel.city_id == city_id,
                ),
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as exception:
            logger.error(f"Failed to remove favorite city: {exception}")
            raise exception

    async def toggle_notifications(self, user_id: UUID4, city_id: int) -> None:
        """
        Toggle notifications for a city.

        :param user_id: ID of the user.
        :param city_id: ID of the city.

        :raises FavoriteCityNotFoundError: If the city is not found in favorites.
        :raises Exception: If there is an error during notifications toggle.
        """
        try:
            select_stmt = select(FavoriteCityModel).where(
                and_(
                    FavoriteCityModel.user_id == user_id,
                    FavoriteCityModel.city_id == city_id,
                ),
            )
            result = await self.session.execute(select_stmt)
            favorite_city = result.scalar()
            if favorite_city is None:
                raise FavoriteCityNotFoundError(
                    detail="City not found in favorites.",
                )
            update_stmt = (
                update(FavoriteCityModel)
                .where(
                    and_(
                        FavoriteCityModel.user_id == user_id,
                        FavoriteCityModel.city_id == city_id,
                    ),
                )
                .values(
                    allow_notifications=not favorite_city.allow_notifications,
                )
            )
            await self.session.execute(update_stmt)
            await self.session.commit()
        except Exception as exception:
            logger.error(f"Failed to toggle notifications: {exception}")
            raise exception
