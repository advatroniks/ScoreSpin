import uuid

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.alive_connections: {uuid.UUID: list[WebSocket]} = {}

    async def connect(
            self,
            websocket: WebSocket,
            tournament_id: uuid.UUID,
            user_id: int
    ):
        await websocket.accept()
        if tournament_id in self.alive_connections:
            self.alive_connections[tournament_id].append(user_id, websocket)
        else:
            self.alive_connections[tournament_id] = [websocket]

    async def update_table_conditions_for_all_users(
            self,
            table_conditions: dict,
            tournament_id: uuid.UUID
    ):
        if tournament_id in self.alive_connections:
            for client_websocket in self.alive_connections[tournament_id]:
                client_websocket[1].send_json(table_conditions)

    async def update_current_game(self):
        pass

    def disconnect(self, websocket: WebSocket, tournament_id: uuid.UUID):
        self.alive_connections[tournament_id].remove(websocket)





