from fastapi import APIRouter
from db_manager.schemas import ResponseSchema, Question

from services.ai_service import AIService

router = APIRouter()

@router.post("/generate", response_model=ResponseSchema)
def generate_text(question: Question):
    ai_service = AIService()
    ans = ai_service.generate_text(question.question)
    return ResponseSchema(
        status="success",
        status_code=200,
        message="Text generated successfully",
        payload=ans
    )
