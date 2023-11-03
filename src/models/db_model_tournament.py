from typing import Literal, TYPE_CHECKING
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .db_model_profile import Profile


class Tournament(Base):
    tournament_type: Mapped[Literal["standard", "extend"]]
    tournament_date: Mapped[date]
    tournament_coefficient: Mapped[float] = mapped_column(
        nullable=True
    )
    players_profiles: Mapped[list["Profile"]] = relationship(
        secondary="players_tournaments_m2m",
        back_populates="tournaments"
    )

