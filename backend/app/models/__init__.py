from .board_model import BoardCreate, BoardModel, BoardUpdate
from .shape_model import Point, StrokeData, ShapeResponse
from .math_model import MathRequest, MathResponse
from .diagram_model import DiagramElement, DiagramConnection, DiagramRequest, DiagramResponse
from .topic_model import TopicRequest, TopicResponse

# Export everything for clean 'from app.models import ...' syntax
__all__ = [
    "BoardCreate", "BoardModel", "BoardUpdate",
    "Point", "StrokeData", "ShapeResponse",
    "MathRequest", "MathResponse",
    "DiagramElement", "DiagramConnection", "DiagramRequest", "DiagramResponse",
    "TopicRequest", "TopicResponse"
]
