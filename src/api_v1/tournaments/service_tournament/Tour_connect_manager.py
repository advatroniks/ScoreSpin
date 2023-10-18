import uuid

from fastapi import WebSocket

from .Tour_schemas import TournamentUpdateAll, TournamentUpdateActiveGame, CurrentGameData


class ConnectionManager:
    def __init__(self):
        self.alive_connections: {int: list[WebSocket]} = {}

    async def connect(
            self,
            websocket: WebSocket,
            tournament_id: int,
            user_id: int
    ):
        await websocket.accept()
        if tournament_id in self.alive_connections:
            self.alive_connections[tournament_id].append((user_id, websocket))
        else:
            self.alive_connections[tournament_id] = [(user_id, websocket)]

        for key, value in self.alive_connections.items():
            print(key, value, "test_VALUE_DICT")

    async def update_table_conditions_for_all_users(
            self,
            tournament_id: int,  # MOCK FOR TESTING  ONLY UUID FIELD
            table_conditions: dict,
    ):

        data_serialize = {}
        for key, value in table_conditions.items():
            data_serialize[key] = [i.pid for i in value]

        if tournament_id in self.alive_connections:
            for client_websocket in self.alive_connections[tournament_id]:
                if client_websocket[0] in data_serialize:
                    current_play = table_conditions[client_websocket[0]]
                    current_play_tuple = [(value[0], value[1], key) for key, value in current_play.items()]
                    users_data = CurrentGameData(
                        first_player=current_play_tuple[0][0],
                        second_player=current_play_tuple[0][1],
                        table_number=current_play_tuple[0][2]
                    )
                    data = TournamentUpdateActiveGame(
                        all_games_data={key: [value[0].first_name, value[1].first_name] for key, value in table_conditions.items()},
                        current_game=users_data
                    )
                    await client_websocket[1].send_json(data.model_dump())
                else:
                    data = TournamentUpdateAll(
                        all_games_data={key: [value[0].first_name, value[1].first_name] for key, value in table_conditions.items()},
                    )
                    await client_websocket[1].send_json(data.model_dump())

    async def update_current_game(
            self,
            tournament_id: int,  # MOCK FOR TESTING ONLY UUID FIELD
            user_id: int,
            data: TournamentUpdateAll
    ):
        pass


    def disconnect(self, websocket: WebSocket, tournament_id: uuid.UUID):
            self.alive_connections[tournament_id].remove(websocket)


connection_manager = ConnectionManager()