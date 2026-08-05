from datetime import datetime
from pathlib import Path


LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "llm_requests.log"


def log_llm_request(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    cost: float | None,
) -> None:
    LOG_DIRECTORY.mkdir(exist_ok=True)

    timestamp = datetime.now().isoformat(timespec="seconds")
    formatted_cost = f"${cost:.8f}" if cost is not None else "Unavailable"

    log_entry = (
        "========================================\n"
        f"Time: {timestamp}\n"
        f"Model: {model}\n"
        f"Prompt Tokens: {prompt_tokens}\n"
        f"Completion Tokens: {completion_tokens}\n"
        f"Total Tokens: {total_tokens}\n"
        f"Cost: {formatted_cost}\n"
        "========================================\n\n"
    )

    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(log_entry)