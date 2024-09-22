from mdpi_api.db.base import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String


class CityModel(Base):
    """Model for cities table object."""

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        BigInteger(),
        autoincrement=True,
        primary_key=True,
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(), nullable=False, index=True)

    # Relationships
    weather = relationship("WeatherModel", back_populates="city")
    favorite_cities = relationship("FavoriteCityModel", back_populates="city")

    def __str__(self) -> str:
        """
        Return string representation of the city model.

        :return: String representation of the city model.
        """
        return f"<CityModel {self.id}>"
