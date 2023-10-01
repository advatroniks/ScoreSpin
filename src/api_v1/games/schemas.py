import uuid

from pydantic import BaseModel, ConfigDict, Field, computed_field, validator, ValidationError
from pydantic_core.core_schema import FieldValidationInfo


class GameBase(BaseModel):
    first_player_id: uuid.UUID
    second_player_id: uuid.UUID
    first_player_score: int = Field(..., ge=0, le=3)
    second_player_score: int = Field(..., ge=0, le=3)


class GameCreate(GameBase):
    @computed_field
    def winner_id(self) -> uuid.UUID:
        if self.first_player_score > self.second_player_score:
            return self.first_player_id
        return self.second_player_id


class GameUpdate(GameCreate):
    pass


class GameUpdatePartial(GameCreate):
    first_player: str | None = None
    second_player: str | None = None
    first_pl_score: str | None = None
    second_pl_score: str | None = None


class Game(GameBase):
    model_config = ConfigDict(
        from_attributes=True)  # Парсим входящую моледль sqlalchemy >> model pydantic.( нужно брать свойства с атрибутов)
    pid: int
