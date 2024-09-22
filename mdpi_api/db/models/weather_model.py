from mdpi_api.db.base import Base
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import JSON


class WeatherModel(Base):
    """Model for weather table object."""

    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(
        BigInteger(),
        autoincrement=True,
        primary_key=True,
        nullable=False,
        index=True,
    )
    city_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("cities.id"),
        nullable=False,
        index=True,
    )
    data: Mapped[MutableDict[str, str]] = mapped_column(
        MutableDict.as_mutable(JSON()),
        nullable=False,
    )

    # Relationships
    city = relationship("CityModel", back_populates="weather")

    def __str__(self) -> str:
        """
        Return string representation of the weather model.

        :return: String representation of the weather model.
        """
        return f"<WeatherModel {self.id}>"
