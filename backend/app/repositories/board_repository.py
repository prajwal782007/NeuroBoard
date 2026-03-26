from datetime import datetime, timezone
from typing import Optional
from app.models.board_model import BoardModel, BoardCreate, BoardUpdate
from app.database.mongo import boards_collection

class BoardRepository:
    async def create_board(self, board_data: BoardCreate) -> BoardModel:
        now = datetime.now(timezone.utc)
        new_board = BoardModel(
            **board_data.model_dump(),
            created_at=now,
            updated_at=now
        )
        
        # Async Motor call safely inserts dict payloads
        await boards_collection.insert_one(new_board.model_dump(by_alias=True))
        return new_board

    async def get_board(self, board_id: str) -> Optional[BoardModel]:
        board = await boards_collection.find_one({"id": board_id})
        if board:
            return BoardModel(**board)
        return None

    async def update_board(self, board_id: str, update_data: BoardUpdate) -> Optional[BoardModel]:
        # Exclude unset dictionary items natively
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        update_dict["updated_at"] = datetime.now(timezone.utc)
        
        # Using return_document=True natively inside pymongo logic to return the mutated row explicitly 
        from pymongo import ReturnDocument
        updated = await boards_collection.find_one_and_update(
            {"id": board_id},
            {"$set": update_dict},
            return_document=ReturnDocument.AFTER
        )
        if updated:
            return BoardModel(**updated)
        return None
