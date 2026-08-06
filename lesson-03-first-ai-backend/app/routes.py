from collections.abc import Generator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import app.llm as llm
from app.conversation import conversation_manager
from app.models import ChatRequest, ChatResponse


router = APIRouter()


@router.get("/")
def read_root():
    return {
        "message": "FastAPI is running!"
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation_manager.add_user_message(request.message)

    answer = llm.ask_llm(
        conversation_manager.get_messages()
    )

    conversation_manager.add_assistant_message(answer)

    return ChatResponse(
        response=answer
    )


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    conversation_manager.add_user_message(request.message)

    def generate() -> Generator[str, None, None]:
        complete_answer = ""

        for chunk in llm.stream_llm(
            conversation_manager.get_messages()
        ):
            complete_answer += chunk
            yield chunk

        conversation_manager.add_assistant_message(
            complete_answer
        )

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )