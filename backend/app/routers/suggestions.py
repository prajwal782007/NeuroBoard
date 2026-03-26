from fastapi import APIRouter, Depends
from app.models.topic_model import TopicRequest, TopicResponse
from app.services.topic_service import TopicService

router = APIRouter(tags=["Suggestions"])

# Singleton instantiation so pytorch models don't reload on every REST call
_topic_service = None

def get_topic_service() -> TopicService:
    global _topic_service
    if _topic_service is None:
        _topic_service = TopicService()
    return _topic_service

@router.post("/analyze-topic", response_model=TopicResponse)
def analyze_topic(request: TopicRequest, service: TopicService = Depends(get_topic_service)):
    """
    NLP route extracting intelligent diagrams from textual descriptions.
    """
    return service.analyze_topic(request)
