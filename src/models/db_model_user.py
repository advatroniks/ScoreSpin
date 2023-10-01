from enum import Enum
from datetime import date
from typing import Literal, TYPE_CHECKING

from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .db_model_profile import Profile


class UserRole(Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class User(Base):
    first_name: Mapped[str]
    surname: Mapped[str]
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true")
    )
    username: Mapped[str] = mapped_column(
        String(length=20),
        nullable=False,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(length=30),
        unique=True
    )
    user_role: Mapped[Literal["admin", "moderator", "user"]] = mapped_column(
        default="user",
        server_default=text("user"),
        nullable=False,
    )

    profile: Mapped["Profile"] = relationship(back_populates="user")
