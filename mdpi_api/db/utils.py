from mdpi_api.settings import settings
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

db_settings = settings.db


async def create_database() -> None:
    """Create a database."""
    db_url = make_url(str(db_settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{db_settings.base}'",  # noqa: E501, S608
            ),
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{db_settings.base}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            ),
        )


async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(db_settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{db_settings.base}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{db_settings.base}"'))
