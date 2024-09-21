from mdpi_api.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String


class DummyModel(Base):
    """Model for demo purpose."""

    __tablename__ = "dummy_model"

    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
