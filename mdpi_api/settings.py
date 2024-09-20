import enum
from pathlib import Path
from tempfile import gettempdir

from decouple import config
from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = config("MDPI_API_HOST", default="0.0.0.0")
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = config("MDPI_API_ENVIRONMENT")

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = config("MDPI_API_DB_HOST")
    db_port: int = config("MDPI_API_DB_PORT", cast=int)
    db_user: str = config("MDPI_API_DB_USER")
    db_pass: str = config("MDPI_API_DB_PASS")
    db_base: str = config("MDPI_API_DB_BASE")
    db_echo: bool = config("MDPI_API_DB_ECHO", cast=bool, default=False)

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "MDPI_API_"
        env_file_encoding = "utf-8"


settings = Settings()
