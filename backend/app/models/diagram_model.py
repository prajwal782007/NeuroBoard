from pydantic import BaseModel
from typing import List, Optional

class DiagramElement(BaseModel):
    id: str
    type: str # e.g., 'circle', 'rectangle', 'diamond'
    label: Optional[str] = ""

class DiagramConnection(BaseModel):
    source_id: str
    target_id: str
    label: Optional[str] = ""

class DiagramRequest(BaseModel):
    elements: List[DiagramElement]
    connections: List[DiagramConnection]

class DiagramResponse(BaseModel):
    mermaid_code: str
