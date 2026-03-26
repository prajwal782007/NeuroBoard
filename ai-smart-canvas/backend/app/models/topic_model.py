from pydantic import BaseModel
from typing import List

class TopicRequest(BaseModel):
    title: str

class TopicResponse(BaseModel):
    topic: str
    suggestions: List[str]
