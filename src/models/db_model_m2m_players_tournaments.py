from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db_model_base import Base


class PlayersTournamentsM2M(Base):
    __tablename__ = "players_tournaments_m2m"
    __table_args__ = (
        UniqueConstraint(
            "profile_pid",
            "tournament_pid",
            name="unique_prof_tour"
        ),
    )

    profile_pid: Mapped[int] = mapped_column(ForeignKey("profiles.pid"))
    tournament_pid: Mapped[int] = mapped_column(ForeignKey("tournaments.pid"))

