"""Answer coach endpoints: /api/coach/question and /analyze"""
from fastapi import APIRouter, HTTPException

from app.schemas.coach import (
    CATEGORIES,
    AnalyzeRequest,
    AnswerAnalysis,
    CategoriesResponse,
    QuestionRequest,
    QuestionResponse,
)
from app.services.coach import analyze_answer, generate_question
from app.services.llm import LLMError

router = APIRouter(prefix="/api/coach", tags=["coach"])


@router.post("/question", response_model=QuestionResponse)
def question(request: QuestionRequest):
    """Returns a random behavioral interview question (optionally tailored to a role)."""
    try:
        return QuestionResponse(question=generate_question(request))
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/analyze", response_model=AnswerAnalysis)
def analyze(request: AnalyzeRequest):
    """Analyzes a draft answer with the STAR method."""
    try:
        return analyze_answer(request)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/categories", response_model=CategoriesResponse)
def categories():
    """The fixed list of themes the user can pick for a random question."""
    return CategoriesResponse(categories=CATEGORIES)
