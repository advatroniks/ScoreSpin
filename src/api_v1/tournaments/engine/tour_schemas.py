from typing import Literal

from pydantic import BaseModel


class CurrentGameData(BaseModel):
    first_player: str
    second_player: str
    table_number: int


class TournamentUpdateAll(BaseModel):
    message_type: Literal["service", "current_game_update", "all_games_update"] = "all_games_update"
    all_games_data: dict | None = None


class TournamentUpdateActiveGame(TournamentUpdateAll):
    current_game: CurrentGameData

