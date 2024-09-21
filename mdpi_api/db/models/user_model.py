import uuid as uuid_lib

from mdpi_api.db.base import Base
from passlib.hash import bcrypt
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import UUID, String


class UserModel(Base):
    """Model for user table object."""

    __tablename__ = "users"

    id: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(),
        insert_default=uuid_lib.uuid4,
        primary_key=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(), nullable=False)

    def verify_password(self, password: str) -> bool:
        """
        Verify the provided password against the stored hashed password.

        :param password: Password to verify.
        :return: True if the password is verified, False otherwise.
        """
        return bcrypt.verify(password, self.password)

    def __str__(self) -> str:
        """
        Return string representation of the user model.

        :return: String representation of the user model.
        """
        return f"<UserModel {self.id}>"
