"""The interview logic: build the prompts and call the model."""
from app.schemas.interview import InterviewFeedback, InterviewSetup, Message
from app.services.llm import generate_structured, generate_text
from app.services.cv_review import round_to_5
from app.services.prompts import INTERVIEWER_PROMPT, LAST_QUESTION_NOTE, FEEDBACK_PROMPT

# ---------------------------- helper functions ------------------------------------

def format_job_description_block(job_description: str) -> str:
    if not job_description:
        return ""
    return (
        "\nTailor the questions to this job description:\n"
        f"<job_description>\n{job_description}\n</job_description>"
    )


def format_interviewer_prompt(setup: InterviewSetup, number: int) -> str:
    is_last = number >= setup.num_questions
    return INTERVIEWER_PROMPT.format(
        role=setup.role,
        number=number,
        total=setup.num_questions,
        last_question_note=LAST_QUESTION_NOTE if is_last else "",
        job_description_block=format_job_description_block(setup),
    )


def format_transcript(history: list[Message]) -> str:
    lines = []
    for message in history:
        who = "Interviewer" if message.role == "assistant" else "Candidate"
        lines.append(f"{who}: {message.content}")
    return "\n\n".join(lines)

# ---------------------------- main functions ------------------------------------


def start_interview(setup: InterviewSetup) -> str:
    """Returns the first question."""
    messages = [
        {"role": "system", "content": format_interviewer_prompt(setup, 1)},
        {"role": "user", "content": "Please start the interview."},
    ]
    return generate_text(messages)

def next_question(setup: InterviewSetup, history: list[Message], number: int) -> str:
    """Returns the next question (a follow-up or a new topic) given the conversation so far."""
    messages = [ {"role": "system", "content": format_interviewer_prompt(setup, number)}]
    messages += [{"role": m.role, "content": m.content} for m in history]        
    return generate_text(messages)


def get_feedback(setup: InterviewSetup, history: list[Message]) -> InterviewFeedback:
    """Evaluates the whole interview."""
    answered = sum(1 for m in history if m.role == "user")
    user_message = (
        f"Target role: {setup.role}\n"
        f"Questions planned: {setup.num_questions}\n"
        f"Answers given: {answered}\n"
    )
    if setup.job_description:
        user_message += f"\n<job_description>\n{setup.job_description}\n</job_description>\n"
    user_message += f"\n<transcript>\n{format_transcript(history)}\n</transcript>"

    messages = [
        {"role": "system", "content": FEEDBACK_PROMPT},
        {"role": "user", "content": user_message},
    ]
    feedback = generate_structured(messages, InterviewFeedback)

    feedback.overall_score = round_to_5(feedback.overall_score)
    return feedback
