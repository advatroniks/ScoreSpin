from typing import Literal
from datetime import date

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Tournament(Base):
    tournament_type: Mapped[Literal["standard", "extend"]]
    tournament_date: Mapped[date]
