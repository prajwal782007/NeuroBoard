from app.models.shape_model import StrokeData, ShapeResponse
from app.ai.shape_detection.detector import ShapeDetector

class ShapeService:
    def __init__(self):
        self.detector = ShapeDetector()

    def process_stroke(self, stroke: StrokeData) -> ShapeResponse:
        points = [{"x": p.x, "y": p.y} for p in stroke.points]
        result = self.detector.detect(points)
        
        return ShapeResponse(
            type=result["type"],
            x=result["x"],
            y=result["y"],
            width=result["width"],
            height=result["height"],
            confidence=0.95
        )
