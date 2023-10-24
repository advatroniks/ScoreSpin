import uuid
from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .db_model_user import User


class Profile(Base):
    base: Mapped[str | None]
    left_side: Mapped[str | None]
    right_side: Mapped[str| None]
    game_style: Mapped[bool| None]
    date_of_birth: Mapped[date| None]
    city: Mapped[str| None]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    rating: Mapped[int] = mapped_column(default=100, server_default=text("100"))
    user: Mapped["User"] = relationship(back_populates="profile")
