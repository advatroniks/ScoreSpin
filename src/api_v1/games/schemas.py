import uuid

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, ValidationError


class GameBase(BaseModel):
    first_player_id: uuid.UUID = Field(..., exclude=True)
    second_player_id: uuid.UUID = Field(..., exclude=True)
    first_player_score: int = Field(..., ge=0, le=3, exclude=True)
    second_player_score: int = Field(..., ge=0, le=3, exclude=True)


class GameCreate(GameBase):
    @computed_field
    @property
    def winner_player_id(self) -> uuid.UUID:
        if self.first_player_score > self.second_player_score:
            return self.first_player_id
        return self.second_player_id

    @computed_field
    @property
    def looser_player_id(self) -> uuid.UUID:
        if self.first_player_score > self.second_player_score:
            return self.second_player_id
        return self.first_player_id

    @computed_field
    @property
    def winner_score(self) -> int:
        if self.first_player_score > self.second_player_score:
            return self.first_player_score
        return self.second_player_score

    @computed_field
    @property
    def looser_score(self) -> int:
        if self.first_player_score > self.second_player_score:
            return self.second_player_score
        return self.first_player_score


class GameUpdate(GameBase):
    first_player_id: uuid.UUID | None = None
    second_player_id: uuid.UUID | None = None
    first_player_score: int | None = None
    second_player_score: int | None = None
    winner_id: uuid.UUID | None = None


class Game(BaseModel):
    # Парсинг входящей модели sqlalchemy >> model pydantic.( нужно брать свойства с атрибутов)
    model_config = ConfigDict(
        from_attributes=True
    )
    pid: int
    id: uuid.UUID
    winner_player_id: uuid.UUID