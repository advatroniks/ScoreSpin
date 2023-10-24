from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from .db_model_base import Base
from typing import Annotated


class Game(Base):
    winner_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id"),
        nullable=False,
    )
    loser_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id"),
        nullable=False,
    )

    winner_score: Mapped[int]
    loser_score: Mapped[int]
