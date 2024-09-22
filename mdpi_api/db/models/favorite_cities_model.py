import uuid

from mdpi_api.db.base import Base
from sqlalchemy import UUID, BigInteger, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FavoriteCityModel(Base):
    """Model for favorite_cities table object."""

    __tablename__ = "favorite_cities"

    id: Mapped[int] = mapped_column(
        Integer(),
        autoincrement=True,
        primary_key=True,
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    city_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    allow_notifications: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False,
    )

    # Relationships
    user = relationship("UserModel", back_populates="favorite_cities")
    city = relationship("CityModel", back_populates="favorite_cities")

    def __str__(self) -> str:
        """
        Return string representation of the favorite city model.

        :return: String representation of the favorite city model.
        """
        return f"<FavoriteCityModel {self.id}>"
