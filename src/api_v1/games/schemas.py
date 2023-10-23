import uuid

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, ValidationError
from pydantic_core.core_schema import FieldValidationInfo


class GameBase(BaseModel):
    winner_id: uuid.UUID
    loser_id: uuid.UUID
    winner_score: int = Field(..., ge=0, le=3)
    loser_score: int = Field(..., ge=0, le=3)


class GameCreate(BaseModel):
    first_player_id: uuid.UUID
    second_player_id: uuid.UUID
    first_player_score: int
    second_player_score: int

    @computed_field
    @property
    def winner_id(self) -> uuid.UUID:
        if self.second_player_score_score > self.first_player_score:
            return self.second_player_id
        return self.first_player_id

    @computed_field
    @property
    def loser_id(self) -> uuid.UUID:
        if self.winner_id == self.first_player_id:
            return self.second_player_id
        return self.first_player_id

    @computed_field
    @property
    def winner_score(self) -> int:
        if self.second_player_score_score > self.first_player_score:
            return self.second_player_score
        return self.first_player_score

    @computed_field
    @property
    def loser_score(self) -> int:
        if self.second_player_score_score < self.first_player_score:
            return self.second_player_score
        return self.first_player_score

class GameUpdate(GameBase):
    winner_id: uuid.UUID | None = None
    loser_id: uuid.UUID | None = None
    winner_score: int | None = None
    loser_score: int | None = None


class Game(GameBase):

    # Парсинг входящей модели sqlalchemy >> model pydantic.( нужно брать свойства с атрибутов)
    model_config = ConfigDict(
        from_attributes=True
    )
    pid: int
