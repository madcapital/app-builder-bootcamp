conversation = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Answer clearly and concisely."
        ),
    }
]


def add_user_message(message: str) -> None:
    conversation.append(
        {
            "role": "user",
            "content": message,
        }
    )


def add_assistant_message(message: str) -> None:
    conversation.append(
        {
            "role": "assistant",
            "content": message,
        }
    )


def get_conversation() -> list[dict[str, str]]:
    return conversation