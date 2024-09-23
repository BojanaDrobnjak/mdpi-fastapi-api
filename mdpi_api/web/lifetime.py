from typing import Awaitable, Callable

from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from loguru import logger
from mdpi_api.db.meta import meta
from mdpi_api.db.models import load_all_models
from mdpi_api.db.seeders.initial_data import seed_data
from mdpi_api.services.scheduler_service import SchedulerManager
from mdpi_api.services.weather_service import WeatherService
from mdpi_api.settings import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

db_settings = settings.db


async def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(db_settings.db_url), echo=db_settings.echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    # Check if the connection has been established
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        logger.info("Database connection established.")
    except Exception as exception:
        logger.error(f"Failed to establish database connection: {exception}")


async def _create_tables() -> None:  # pragma: no cover
    """Populates tables in the database."""
    load_all_models()
    engine = create_async_engine(str(db_settings.db_url))
    async with engine.begin() as connection:
        await connection.run_sync(meta.create_all)
    await engine.dispose()


def _register_scheduled_events(session: AsyncSession) -> None:
    """
    Register scheduled events.

    :param session: database session.
    """
    scheduler = SchedulerManager()
    weather_service = WeatherService(session)
    scheduler.add_job(
        func=weather_service.update_weather_for_all_cities,
        trigger=CronTrigger(hour="*", minute=0),  # Runs every hour
    )
    scheduler.start()


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        await _setup_db(app)
        # await _create_tables()
        app.middleware_stack = app.build_middleware_stack()
        async with app.state.db_session_factory() as session:
            await seed_data(session)
            _register_scheduled_events(session)

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()

        pass  # noqa: WPS420

    return _shutdown
