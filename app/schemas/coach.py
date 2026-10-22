"""Shapes of the data used by the answer coach endpoints."""
from typing import Literal
from pydantic import BaseModel, Field, field_validator


# The fixed list of themes. The UI loads it
# from GET /api/coach/categories and the server validates against it.
CATEGORIES = [
    "working in a team", "handling a conflict with a colleague", "learning from a failure",
    "meeting a tight deadline", "taking initiative", "dealing with a difficult stakeholder",
    "learning something new quickly", "making a decision with incomplete information",
    "receiving critical feedback", "helping a teammate", "improving a process",
    "handling several priorities at once", "working with unclear requirements",
    "making a mistake and fixing it", "persuading someone to change their mind",
]


class QuestionRequest(BaseModel):
    role: str | None = Field(default=None, max_length=100)           # optional, tailors the question
    category: str | None = Field(default=None, max_length=100)  

    @field_validator("category")
    @classmethod
    def category_must_be_known(cls, value: str | None) -> str | None:
        if value is not None and value not in CATEGORIES:
            raise ValueError("Unknown category")
        return value


class QuestionResponse(BaseModel):
    question: str


class CategoriesResponse(BaseModel):
    categories: list[str]


class AnalyzeRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    answer: str = Field(min_length=10, max_length=4000)
    role: str | None = Field(default=None, max_length=100)

    @field_validator("question", "answer")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value

class STARComponent(BaseModel):
    name: Literal["Situation", "Task", "Action", "Result"]
    status: Literal["strong", "partial", "missing"]
    found_text: str = Field(
        description="Sentences copied word for word from the draft that belong to this part, or empty text"
    )
    whats_missing: str = Field(description="What is missing or unclear in this part")
    why_it_matters: str = Field(description="Why an interviewer cares about this part")
    how_to_improve: str = Field(description="A concrete suggestion to improve this part")
    guiding_questions: list[str] = Field(
        description="2-3 short questions the candidate can answer from real experience to fill the gap"
    )


class AnswerAnalysis(BaseModel):
    score: int = Field(description="Score from 0 to 100")
    summary: str = Field(description="2-3 sentence overall assessment")
    components: list[STARComponent] = Field(description="Exactly four items: Situation, Task, Action, Result")
    start_with: Literal["Situation", "Task", "Action", "Result"] = Field(
        description="The weakest part, which the candidate should fix first"
    )
    extra_tips: list[str] = Field(description="Up to 3 tips about length, specificity, 'I' vs 'we', relevance")
