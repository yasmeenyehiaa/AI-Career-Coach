"""Interview endpoints: /api/interview/start, /answer and /feedback"""
from fastapi import APIRouter, HTTPException

from app.schemas.interview import (
    AnswerRequest,
    AnswerResponse,
    FeedbackRequest,
    InterviewFeedback,
    InterviewSetup,
    StartResponse,
)
from app.services.interview import get_feedback, next_question, start_interview
from app.services.llm import LLMError

router = APIRouter(prefix="/api/interview", tags=["interview"])

@router.post("/start", response_model=StartResponse)
def start(setup: InterviewSetup):
    """The user sends the role (and optional job description), we send the first question."""
    try:
        return StartResponse(question=start_interview(setup))
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/answer", response_model=AnswerResponse)
def answer(request: AnswerRequest):
    """(repeated): the frontend sends the whole conversation, ending with the
    candidate's latest answer. We send the next question, or finished=True."""
    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="The last message must be the candidate's answer.")

    questions_asked = sum(1 for m in request.messages if m.role == "assistant")
    if questions_asked >= request.num_questions:
        return AnswerResponse(question=None, finished=True)

    try:
        question = next_question(request, request.messages, questions_asked + 1)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return AnswerResponse(question=question, finished=False)


@router.post("/feedback", response_model=InterviewFeedback)
def feedback(request: FeedbackRequest):
    """Step 3: evaluate the full conversation."""
    if not any(m.role == "user" for m in request.messages):
        raise HTTPException(status_code=400, detail="Answer at least one question to get feedback.")
    try:
        return get_feedback(request, request.messages)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))
