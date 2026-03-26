from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime, timezone

class BoardCreate(BaseModel):
    id: str
    title: str
    elements: List[Any] = []

class BoardModel(BoardCreate):
    created_at: datetime
    updated_at: datetime

class BoardUpdate(BaseModel):
    title: Optional[str] = None
    elements: Optional[List[Any]] = None
