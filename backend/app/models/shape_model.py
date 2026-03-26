from pydantic import BaseModel
from typing import List, Optional

class Point(BaseModel):
    x: float
    y: float

class StrokeData(BaseModel):
    points: List[Point]

class ShapeResponse(BaseModel):
    type: str # 'rectangle', 'circle', 'diamond', 'arrow', 'line', 'unknown'
    x: float
    y: float
    width: float
    height: float
    confidence: Optional[float] = 1.0
