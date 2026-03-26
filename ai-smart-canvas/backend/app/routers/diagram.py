from fastapi import APIRouter, Depends
from app.models.diagram_model import DiagramRequest, DiagramResponse
from app.services.diagram_service import DiagramService

router = APIRouter(tags=["Diagram"])

def get_diagram_service():
    return DiagramService()

@router.post("/generate-diagram", response_model=DiagramResponse)
def generate_diagram(
    request: DiagramRequest, 
    service: DiagramService = Depends(get_diagram_service)
):
    """
    Takes scattered logical canvas nodes and outputs formal Mermaid.js flowchart code.
    """
    return service.generate_mermaid(request)
