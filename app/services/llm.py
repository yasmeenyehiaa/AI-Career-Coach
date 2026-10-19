"""The ONLY file that talks to OpenAI. Everything else calls this."""
from openai import OpenAI
from app.config import get_settings


class LLMError(Exception):
    """Something went wrong while calling the model."""

def generate_structured_messages(messages: list[dict], schema):
    """Send messages to the model and get back an object of type `schema`."""
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key, timeout=40)

    try: 
        response = client.chat.completions.parse(
            model=settings.openai_model,
            messages=messages,
            response_format=schema,
        )
    except Exception as e:
        raise LLMError(f"OpenAI request failed: {e}")

    result = response.choices[0].message.parsed
    if result is None: 
        raise LLMError("The model did not return a valid answer.")
    return result