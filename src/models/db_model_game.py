from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from .db_model_base import Base
from typing import Annotated


class Game(Base):
    first_player_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id"),
        nullable=False,
    )
    second_player_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id"),
        nullable=False,
    )

    winner_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id"),
        nullable=False,
    )

    first_player_score: Mapped[int]
    second_player_score: Mapped[int]
