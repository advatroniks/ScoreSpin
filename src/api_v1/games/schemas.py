import uuid

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, ValidationError
from pydantic_core.core_schema import FieldValidationInfo


class GameBase(BaseModel):
    first_player_id: uuid.UUID
    second_player_id: uuid.UUID
    first_player_score: int = Field(..., ge=0, le=3)
    second_player_score: int = Field(..., ge=0, le=3)


class GameCreate(GameBase):

    @computed_field
    @property
    def winner_id(self) -> uuid.UUID:
        if self.first_player_score > self.second_player_score:
            return self.first_player_id
        return self.second_player_id


class GameUpdate(GameBase):
    first_player_id: uuid.UUID | None = None
    second_player_id: uuid.UUID | None = None
    first_player_score: int | None = None
    second_player_score: int | None = None
    winner_id: uuid.UUID | None = None


class Game(GameBase):

    # Парсинг входящей модели sqlalchemy >> model pydantic.( нужно брать свойства с атрибутов)
    model_config = ConfigDict(
        from_attributes=True
    )
    pid: int
