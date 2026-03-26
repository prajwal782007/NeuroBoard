from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        """
        Manages real-time WebSocket connections segregated by unique board instances.
        """
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, board_id: str):
        # Accept incoming WS
        await websocket.accept()
        
        # Initialize room if it doesn't exist
        if board_id not in self.active_connections:
            self.active_connections[board_id] = []
            
        self.active_connections[board_id].append(websocket)

    def disconnect(self, websocket: WebSocket, board_id: str):
        if board_id in self.active_connections:
            if websocket in self.active_connections[board_id]:
                self.active_connections[board_id].remove(websocket)
            
            # Clean up empty rooms
            if not self.active_connections[board_id]:
                del self.active_connections[board_id]

    async def broadcast(self, message: dict, board_id: str, exclude: WebSocket = None):
        """
        Sends state updates to every client connected to the specific board.
        Excludes the original sender to prevent infinite loops.
        """
        if board_id in self.active_connections:
            for connection in self.active_connections[board_id]:
                if connection != exclude:
                    try:
                        await connection.send_json(message)
                    except Exception:
                        pass # Ignore broken pipes

manager = ConnectionManager()
