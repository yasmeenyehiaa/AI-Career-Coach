"""The ONLY file that talks to OpenAI. Everything else calls this."""
from openai import OpenAI
from app.config import get_settings
from app.schemas.interview import InterviewSetup


class LLMError(Exception):
    """Something went wrong while calling the model."""

def create_client() -> OpenAI:
    return OpenAI(api_key=get_settings().openai_api_key, timeout=60)  # 60s timeout


def generate_review_messages(messages: list[dict], schema):
    """Send messages to the model and get back an object of type `schema`."""
    try: 
        response = create_client().chat.completions.parse(
            model=get_settings().openai_model,
            messages=messages,
            response_format=schema,
        )
    except Exception as e:
        raise LLMError(f"OpenAI request failed: {e}")

    result = response.choices[0].message.parsed
    if result is None: 
        raise LLMError("The model did not return a valid answer.")
    return result



def generate_interview_messages(messages: list[dict]):
    """Plain text answer (used for the interviewer's questions)."""
    try:
        response = create_client().chat.completions.create(
            model=get_settings().openai_model,
            messages=messages,
        )
    except Exception as e:
        raise LLMError(f"OpenAI request failed: {e}")

    result = response.choices[0].message.content
    if result is None:
        raise LLMError("The model did not return a valid answer.")
    return result
