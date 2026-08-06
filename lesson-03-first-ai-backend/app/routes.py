from collections.abc import Generator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import app.conversation as conversation
import app.llm as llm


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.get("/")
def read_root():
    return {
        "message": "FastAPI is running!"
    }


@router.post("/chat")
def chat(request: ChatRequest):
    conversation.add_user_message(request.message)

    answer = llm.ask_llm(
        conversation.get_conversation()
    )

    conversation.add_assistant_message(answer)

    return {
        "response": answer
    }


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    conversation.add_user_message(request.message)

    def generate() -> Generator[str, None, None]:
        complete_answer = ""

        for chunk in llm.stream_llm(
            conversation.get_conversation()
        ):
            complete_answer += chunk
            yield chunk

        conversation.add_assistant_message(complete_answer)

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )