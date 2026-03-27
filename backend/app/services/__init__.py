from .shape_service import ShapeService
from .math_service import MathService
from .diagram_service import DiagramService
from .topic_service import TopicService
from .connection_manager import manager

# Simplified service exports
__all__ = [
    "ShapeService",
    "MathService",
    "DiagramService",
    "TopicService",
    "manager"
]
