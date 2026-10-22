"""Builds the prompt for the CV review and calls the LLM."""
from app.schemas.cv import CVResponse, CVRequest
from app.services.llm import generate_structured
from app.services.prompts import CV_PROMPT

def round_to_5(value: float) -> int:
    """Clamp to 0-100 and round to the nearest multiple of 5 (removes small noise)."""
    value = max(0, min(100, value))
    return int(value / 5 + 0.5) * 5


def review_cv(request: CVRequest) -> CVResponse:
    # Wrap untrusted text in tags so the model can tell data from instructions
    user_message = f"Target role: {request.role}\n\n<cv>\n{request.cv_text}\n</cv>"
    if request.job_description:
        user_message += f"\n\n<job_description>\n{request.job_description}\n</job_description>"

    messages = [
        {"role": "system", "content": CV_PROMPT},
        {"role": "user", "content": user_message},
    ]
    review = generate_structured(messages, CVResponse)

    for section in review.sections:
        section.score = round_to_5(section.score)

    if review.sections:
        average = sum(s.score for s in review.sections) / len(review.sections)
        review.overall_score = round_to_5(average)
    else:
        review.overall_score = round_to_5(review.overall_score)

    return review
