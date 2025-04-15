import json
from fastapi.websockets import WebSocket
from typing import List

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str, msg_type: str = "info"):
        payload = json.dumps({"type": msg_type, "message": message})
        for connection in self.active_connections:
            await connection.send_text(payload)
