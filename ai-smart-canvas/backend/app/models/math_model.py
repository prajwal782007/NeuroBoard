from pydantic import BaseModel
from typing import Optional

class MathRequest(BaseModel):
    image_base64: str

class MathResponse(BaseModel):
    equation: str
    solution: str
    error: Optional[str] = None
