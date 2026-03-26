from fastapi import APIRouter, Depends
from app.models.shape_model import StrokeData, ShapeResponse
from app.services.shape_service import ShapeService

router = APIRouter(
    prefix="/canvas",
    tags=["Canvas"]
)

# Dependency injection for the service
def get_shape_service():
    return ShapeService()

@router.post("/detect-shapes", response_model=ShapeResponse)
def detect_shapes(stroke: StrokeData, service: ShapeService = Depends(get_shape_service)):
    """
    Receives stroke data (list of points) and returns the classified shape.
    """
    return service.process_stroke(stroke)
