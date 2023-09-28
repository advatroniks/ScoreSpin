from enum import Enum
from typing import Annotated
from sqlalchemy import CheckConstraint

from sqlalchemy.orm import Mapped, mapped_column
from src.models import Base
from sqlalchemy import Boolean, String, text


class UserRole(Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class User(Base):
    first_name: Mapped[str]
    surname: Mapped[str]
    age: Mapped[int]
    city: Mapped[str]
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
    user_role: Mapped[str] = mapped_column(
        default="user",
        server_default=text("user"),
        nullable=False,
    )




