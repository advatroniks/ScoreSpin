from sqlalchemy import ForeignKey, Uuid as AlchemyUUID
from sqlalchemy.orm import Mapped, mapped_column

from .db_model_base import Base


class Game(Base):
    winner_player_id: Mapped[str] = mapped_column(
        AlchemyUUID,
        ForeignKey("users.id"),
        nullable=False
    )
    looser_player_id: Mapped[str] = mapped_column(
        AlchemyUUID,
        ForeignKey("users.id"),
        nullable=False
    )

    winner_score: Mapped[int]
    looser_score: Mapped[int]

