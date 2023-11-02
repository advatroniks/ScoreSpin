from datetime import datetime

from sqlalchemy import Uuid as AlchemyUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db_model_base import Base
from .db_model_game import Game


class Rating(Base):
    profile_pid: Mapped[int] = mapped_column(
        ForeignKey("profiles.pid"),
        nullable=False
    )
    rating_total: Mapped[int]
    rating_diff: Mapped[int]
    rating_registrations: Mapped[datetime]
    game_pid: Mapped[int] = mapped_column(
        ForeignKey("games.pid")
    )
    tournament_pid: Mapped[int] = mapped_column(
        ForeignKey("tournaments.pid")
    )
    game: Mapped["Game"] = relationship()




