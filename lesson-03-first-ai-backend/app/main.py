from fastapi import FastAPI
from pydantic import BaseModel

import app.llm as llm


app = FastAPI()


class ChatRequest(BaseModel):
    message: str


conversation = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Answer clearly and concisely."
        ),
    }
]


@app.get("/")
def read_root():
    return {
        "message": "FastAPI is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    conversation.append(
        {
            "role": "user",
            "content": request.message,
        }
    )

    answer = llm.ask_llm(conversation)

    conversation.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return {
        "response": answer
    }