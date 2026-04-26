import uuid
import os
import time
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import FastAPI, Cookie, Response, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import RateLimitError

import conversation

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

RATE_LIMIT = 20        # max messages per session
RATE_WINDOW = 3600     # per hour (seconds)

# {session_id: [timestamp, ...]}
_rate_store: dict[str, list[float]] = defaultdict(list)


def is_rate_limited(session_id: str) -> bool:
    now = time.time()
    timestamps = _rate_store[session_id]
    # drop entries outside the window
    _rate_store[session_id] = [t for t in timestamps if now - t < RATE_WINDOW]
    if len(_rate_store[session_id]) >= RATE_LIMIT:
        return True
    _rate_store[session_id].append(now)
    return False


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.post("/api/chat")
async def chat(req: ChatRequest, response: Response, session_id: str = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie("session_id", session_id, httponly=True, samesite="lax")

    if is_rate_limited(session_id):
        raise HTTPException(status_code=429, detail="You've sent a lot of messages! Take a breather and try again in an hour.")

    try:
        reply = conversation.chat(session_id=session_id, text=req.message)
    except RateLimitError:
        raise HTTPException(status_code=503, detail="BrewBot is taking a short break — the AI service is at capacity. Try again in a few minutes! ☕")
    return {"reply": reply, "session_id": session_id}


@app.post("/api/reset")
async def reset(response: Response, session_id: str = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    try:
        reply = conversation.start_session(session_id)
    except RateLimitError:
        reply = "Hey! I'm BrewBot ☕ — taking a short break right now. Try again in a few minutes!"
    response.set_cookie("session_id", session_id, httponly=True, samesite="lax")
    return {"reply": reply, "session_id": session_id}
