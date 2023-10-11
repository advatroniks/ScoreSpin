import uuid
from enum import Enum

from pydantic import BaseModel, Field


class TournamentTypeEnum(str, Enum):
    standard = "standard"
    extend = "extend"


class CreateTournament(BaseModel):
    members: list[uuid.UUID]
    table_counts: int | list[int]
    tournament_type: TournamentTypeEnum
