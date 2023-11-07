from datetime import datetime

from sqlalchemy import ForeignKey, Uuid as AlchemyUUID, DATETIME, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db_model_base import Base
from .db_model_profile import Profile


class Game(Base):
    winner_profile_pid: Mapped[str] = mapped_column(
        AlchemyUUID,
        ForeignKey("profile.pid"),
        nullable=False
    )
    looser_profile_pid: Mapped[str] = mapped_column(
        AlchemyUUID,
        ForeignKey("profile.pid"),
        nullable=False
    )
    winner_score: Mapped[int]
    looser_score: Mapped[int]

    tournament_pid: Mapped[int] = mapped_column(
        ForeignKey("tournaments.pid"),
        nullable=True
    )

    game_time: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=text("now()"),
        nullable=False
    )
