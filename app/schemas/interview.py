"""Shape of the data the interview endpoint returns."""
from pydantic import BaseModel, Field
from typing import Literal

class InterviewSetup(BaseModel):
    """The settings chosen by the user. The frontend sends them with every request,
    because the server keeps no memory between requests."""
    role: str = Field(max_length=200)
    job_description: str | None = Field(max_length=5000)
    num_questions: int = Field(default=6, ge=3, le=10)

class Message(BaseModel):
    """One message of the conversation."""
    role: Literal["assistant", "user"]   # assistant = interviewer, user = candidate
    content: str = Field(min_length=1, max_length=4000)

class StartResponse(BaseModel):
    question: str

class AnswerRequest(InterviewSetup):
    messages: list[Message] = Field(min_length=1, max_length=40)   # the whole conversation so far

class AnswerResponse(BaseModel):
    question: str | None
    finished: bool

class FeedbackRequest(AnswerRequest):
    """Same fields as AnswerRequest"""

class AnswerImprovement(BaseModel):
    question: str = Field(description="The interview question (shortened if long)")
    issue: str = Field(description="What was weak or missing in the candidate's answer")
    how_to_improve: str = Field(description="Concrete advice, with an example of what to say")

class InterviewFeedback(BaseModel):
    overall_score: int = Field(description="Overall performance score from 0 to 100")
    summary: str = Field(description="2-3 sentence overall assessment")
    strengths: list[str]
    weaknesses: list[str]
    answer_improvements: list[AnswerImprovement] = Field(
        description="The answers that need the most improvement"
    )