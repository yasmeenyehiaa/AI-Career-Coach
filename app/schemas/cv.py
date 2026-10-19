"""Shape of the data the CV review endpoint returns."""
from pydantic import BaseModel, Field

class CVRequest(BaseModel):
    cv_text: str
    role: str = Field(max_length=200)
    job_description: str | None = Field(max_length=5000)


class SectionFeedback(BaseModel):
    name: str = Field(description="One of: content, clarity, formatting, errors, skills")
    score: int = Field(description="Score from 0 to 100")
    strengths: list[str]
    suggestions: list[str] = Field(description="Specific, actionable improvements")


class CVResponse(BaseModel):
    overall_score: int = Field(description="Overall score from 0 to 100")
    summary: str = Field(description="2-3 sentence overall assessment")
    sections: list[SectionFeedback]
    missing_skills: list[str] = Field(description="Skills the role needs that the CV lacks")
    top_priorities: list[str] = Field(description="The 3 most important fixes, in order")
