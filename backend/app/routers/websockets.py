from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.connection_manager import manager

router = APIRouter(tags=["Realtime"])

@router.websocket("/ws/{board_id}")
async def websocket_endpoint(websocket: WebSocket, board_id: str):
    """
    Handles live canvas edits spanning drawing lines, erasing nodes, scaling shapes.
    """
    await manager.connect(websocket, board_id)
    try:
        while True:
            # Expecting dict payloads like: {"event": "draw", "data": {"x": 100, ...}}
            data = await websocket.receive_json()
            
            # Rebroadcast payload directly to peer clients attached to this exact board
            await manager.broadcast(data, board_id, exclude=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, board_id)
        # Notify others anonymously that an author dropped
        await manager.broadcast({"event": "user_left", "data": {}}, board_id)
