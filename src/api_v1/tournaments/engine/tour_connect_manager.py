from typing import Literal

from fastapi import WebSocket

from src.models import User
from .tour_schemas import (
    TournamentUpdateAll,
    TournamentUpdateActiveGame,
    CurrentGameData,
)


class ConnectionManager:
    def __init__(self):
        self.alive_connections: {int: list[int, WebSocket]} = {}

    async def connect(self, websocket: WebSocket, tournament_id: int, user_id: int):
        if tournament_id in self.alive_connections:
            self.alive_connections[tournament_id].append((user_id, websocket))
        else:
            self.alive_connections[tournament_id] = [(user_id, websocket)]

        for key, value in self.alive_connections.items():
            print(key, value, "c")

    async def update_table_conditions_for_all_users(
        self,
        tournament_id: int,  # MOCK FOR TESTING  ONLY UUID FIELD
        table_conditions: dict[int, list[User]],
    ):
        connections = self.alive_connections[tournament_id]

        table_conditions_pid = apply_user_method_for_table_conditions(
            table_conditions=table_conditions,
            method="pid"
        )

        for user_websocket in connections:
            current_table_number = check_user_in_table_conditions(
                    table_conditions=table_conditions_pid,
                    user_id=user_websocket[0]
                )
            if current_table_number:
                await user_websocket[1].send_json(
                    TournamentUpdateActiveGame(
                        message_type="current_game_update",
                        all_games_data=apply_user_method_for_table_conditions(
                            table_conditions=table_conditions,
                            method="first_name"
                        ),
                        current_game=CurrentGameData(
                            first_player=table_conditions[current_table_number][0].first_name,
                            second_player=table_conditions[current_table_number][1].first_name,
                            table_number=current_table_number
                        )
                    ).model_dump()
                )

            else:
                await user_websocket[1].send_json(
                    TournamentUpdateAll(
                        all_games_data=apply_user_method_for_table_conditions(
                            table_conditions=table_conditions,
                            method="first_name"
                        )
                    ).model_dump()
                )

    def disconnect(
            self,
            websocket: WebSocket,
            tournament_id: int,
            user_id: int
    ):
        self.alive_connections[tournament_id].remove((user_id, websocket))


connection_manager = ConnectionManager()


def check_user_in_table_conditions(
    table_conditions: dict,
    user_id: int                            # MOCK FOR TESTING
) -> tuple | bool:
    for table, users_list in table_conditions.items():
        if user_id in users_list:
            return table
        else:
            return False


def apply_user_method_for_table_conditions(
        table_conditions: dict[int, list[User]],
        method: Literal["pid", "first_name"] = "pid"
) -> dict:
    table_conditions_translate = {}
    for table, users in table_conditions.items():
        if method == "pid":
            table_conditions_translate[table] = list(map(lambda user: user.pid, users))
        elif method == "first_name":
            table_conditions_translate[table] = list(map(lambda user: user.first_name, users))

    return table_conditions_translate
