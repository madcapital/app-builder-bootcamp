import os

from dotenv import load_dotenv
from openai import OpenAI

from app.logger import log_llm_request


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("LLM_MODEL", "openrouter/auto")

if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY was not found in the environment."
    )


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def ask_llm(messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    usage = response.usage

    if usage is not None:
        log_llm_request(
            model=response.model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            cost=getattr(usage, "cost", None),
        )

    answer = response.choices[0].message.content

    if answer is None:
        raise RuntimeError("The model returned no text response.")

    return answer