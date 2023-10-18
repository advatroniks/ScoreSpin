import uuid

from fastapi import WebSocket

from .Tour_schemas import TournamentUpdate


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
            data: TournamentUpdate
    ):
        if tournament_id in self.alive_connections:
            for client_websocket in self.alive_connections[tournament_id]:
                client_websocket[1].send_json(data)

    async def update_current_game(
            self,
            tournament_id: int,  # MOCK FOR TESTING ONLY UUID FIELD
            user_id: int,
            data: TournamentUpdate
    ):
        pass

    def disconnect(self, websocket: WebSocket, tournament_id: uuid.UUID):
            self.alive_connections[tournament_id].remove(websocket)


connection_manager = ConnectionManager()