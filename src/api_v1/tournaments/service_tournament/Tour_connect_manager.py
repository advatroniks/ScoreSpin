from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.alive_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.alive_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.alive_connections.remove(websocket)



