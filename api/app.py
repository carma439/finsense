import time
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from src.logger import get_logger
from src.agent import agent

logger = get_logger("api")

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    try:
        user_query = req.messages[-1].content
        logger.info(f"Query received: {user_query}")

        start_time = time.time()

        response = agent.invoke({
            "messages": [m.model_dump() for m in req.messages]
        })

        answer = response["messages"][-1].content

        elapsed = time.time() - start_time
        logger.info(f"Response time: {elapsed:.2f}s")

        return {"answer": answer}

    except Exception as e:
        logger.error(f"Error during request: {str(e)}")
        return {"answer": "Something went wrong. Please try again."}