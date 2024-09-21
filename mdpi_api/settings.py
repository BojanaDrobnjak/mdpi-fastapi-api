import enum
from pathlib import Path
from tempfile import gettempdir

from decouple import config
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
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


class LogSettings(BaseModel):
    """Log settings."""

    level: LogLevel = LogLevel.INFO
    path: Path = TEMP_DIR / "api_{time:YYYY-MM-DD}.log"
    rotation: str = "1 day"
    retention: str = "30 days"
    format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>:"
        "<blue>[{correlation_id}]</blue> - <level>{message}</level>"
    )


class DatabaseSettings(BaseModel):
    """Database settings."""

    host: str
    port: int
    user: str
    password: str
    base: str
    echo: bool

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            path=f"/{self.base}",
        )


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    title: str = "MDPI API"
    description: str = "REST API for MDPI"
    host: str = config("MDPI_API_HOST")
    port: int = config("MDPI_API_PORT", cast=int)
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = config("MDPI_API_RELOAD", cast=bool, default=False)

    # Current environment
    environment: str = config("MDPI_API_ENVIRONMENT")

    logging: LogSettings = LogSettings()
    db: DatabaseSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MDPI_API_",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
