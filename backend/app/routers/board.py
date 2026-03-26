from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.board_model import BoardModel, BoardCreate, BoardUpdate
from app.repositories.board_repository import BoardRepository

router = APIRouter(tags=["Board Storage"])
repo = BoardRepository()

@router.post("/save-board", response_model=BoardModel)
async def save_board(board_data: BoardCreate):
    """
    Acts as an Upsert layer. If canvas board ID exists, 
    update the elements. If new, create timestamped entity natively.
    """
    existing = await repo.get_board(board_data.id)
    if existing:
        update_payload = BoardUpdate(title=board_data.title, elements=board_data.elements)
        updated = await repo.update_board(board_data.id, update_payload)
        return updated
        
    return await repo.create_board(board_data)

@router.get("/board/{board_id}", response_model=BoardModel)
async def get_board(board_id: str):
    """
    Read full board config arrays into the frontend cleanly from async Mongo hooks.
    """
    board = await repo.get_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board
