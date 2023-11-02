import uuid
from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .db_model_user import User


class Profile(Base):
    rating: Mapped[int]
    base: Mapped[str | None]
    left_side: Mapped[str | None]
    right_side: Mapped[str | None]
    game_style: Mapped[bool]
    date_of_birth: Mapped[date]
    city: Mapped[str]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="profile")
