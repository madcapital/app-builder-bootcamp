from app.llm import ask_llm
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {
        "message": "FastAPI is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_llm(request.message)

    return {
        "response": answer
    }