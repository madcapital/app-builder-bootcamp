import os

from dotenv import load_dotenv
from openai import OpenAI


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


def ask_llm(message: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Answer clearly and concisely."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    answer = response.choices[0].message.content

    if answer is None:
        raise RuntimeError("The model returned no text response.")

    return answer