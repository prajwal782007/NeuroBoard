from fastapi import APIRouter, Depends
from app.models.math_model import MathRequest, MathResponse
from app.services.math_service import MathService

# Empty prefix so it generates strictly /solve-math as requested
router = APIRouter(tags=["Math"])

def get_math_service():
    return MathService()

@router.post("/solve-math", response_model=MathResponse)
def solve_math(request: MathRequest, service: MathService = Depends(get_math_service)):
    """
    Receives base64 image chunk containing hand-written math and returns solution.
    """
    return service.process_math(request)
