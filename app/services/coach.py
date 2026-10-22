"""The answer coach logic: generate practice questions and analyze answers with STAR."""
import random
from app.schemas.coach import CATEGORIES, AnalyzeRequest, AnswerAnalysis, QuestionRequest
from app.services.llm import generate_structured, generate_text
from app.services.cv_review import round_to_5
from app.services.prompts import ANALYSIS_PROMPT, QUESTION_PROMPT

STAR_ORDER = ["Situation", "Task", "Action", "Result"]

def generate_question(request: QuestionRequest) -> str:
    """Returns one random behavioral interview question."""
    
    user_message = "Write the question."
    if request.role:
        user_message = f"Target role of the candidate: <role> {request.role}\n</role>"

    # The user's category if they chose one, otherwise a random one (so questions still vary)
    theme = request.category or random.choice(CATEGORIES)

    messages = [
        {"role": "system", "content": QUESTION_PROMPT.format(theme=theme)},
        {"role": "user", "content": user_message},
    ]
    # High temperature on purpose: we want variety here
    question = generate_text(messages)
    return question.strip().strip('"“”')


def analyze_answer(request: AnalyzeRequest) -> AnswerAnalysis:
    """Checks a draft answer against STAR and says what to improve."""
    user_message = ""
    if request.role:
        user_message += f"<role>{request.role}</role>\n"
    user_message += f"<question>\n{request.question}\n</question>\n\n<answer>\n{request.answer}\n</answer>"

    messages = [
        {"role": "system", "content": ANALYSIS_PROMPT},
        {"role": "user", "content": user_message},
    ]
    analysis = generate_structured(messages, AnswerAnalysis)

    analysis.score = round_to_5(analysis.score)
    # Make sure the parts always come in STAR order
    analysis.components.sort(key=lambda c: STAR_ORDER.index(c.name))
    return analysis
