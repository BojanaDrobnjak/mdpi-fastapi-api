import uuid
from typing import Any, Dict, Type

from loguru import logger
from mdpi_api.db.base import Base
from mdpi_api.db.models.city_model import CityModel
from mdpi_api.db.models.user_model import UserModel
from mdpi_api.db.seeders.data import cities, users
from mdpi_api.settings import Settings
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

settings = Settings()


async def seed_data(session: AsyncSession) -> None:
    """
    Insert initial data into the database if it doesn't exist.

    :param session: The database session.
    """
    await seed_users(session)
    await seed_cities(session)

    try:
        await session.commit()
        logger.info("Seed data insertion completed.")
    except Exception as ex:
        await session.rollback()
        logger.error(f"Failed to commit seed data: {ex}")


async def seed_users(session: AsyncSession) -> None:
    """
    Insert users into the database if they don't exist.

    :param session: The database session.
    """
    for user in users:
        user_data = {
            "id": uuid.uuid4(),
            "email": user["email"],
            "password": user["password"],
        }
        await insert_if_not_exists(session, UserModel, user_data, "email")


async def seed_cities(session: AsyncSession) -> None:
    """
    Insert cities into the database if they don't exist.

    :param session: The database session.
    """
    for city in cities:
        city_data = {
            "id": city["id"],
            "name": city["name"],
        }
        await insert_if_not_exists(session, CityModel, city_data, "name")


async def insert_if_not_exists(
    session: AsyncSession,
    model: Type[Base],
    data: Dict[str, Any],
    unique_field: str,
) -> None:
    """
    Insert data into the specified model if it doesn't already exist.

    :param session: The database session.
    :param model: The SQLAlchemy model.
    :param data: Data to insert.
    :param unique_field: The field name to check for uniqueness.
    """
    try:
        unique_value = data[unique_field]
        filter_condition = getattr(model, unique_field) == unique_value
        result = await session.execute(select(model).where(and_(filter_condition)))
        existing_record = result.scalars().first()

        if not existing_record:
            new_record = model(**data)
            session.add(new_record)
            logger.info(f"Inserting {model.__name__}: {data[unique_field]}")
    except IntegrityError as ie:
        await session.rollback()
        logger.error(f"Integrity error during seeding {model.__name__}: {ie}")
    except Exception as ex:
        await session.rollback()
        logger.error(f"Failed to seed {model.__name__} data: {ex}")
