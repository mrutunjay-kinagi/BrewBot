import os
from dotenv import load_dotenv
from groq import Groq
from prompts import SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODEL = "llama-3.3-70b-versatile"

# {session_id: [{"role": "user"|"assistant", "content": str}]}
sessions: dict[str, list[dict]] = {}

MAX_HISTORY = 20


def _send(history: list[dict], text: str) -> str:
    history.append({"role": "user", "content": text})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        max_tokens=1024,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply


def start_session(session_id: str) -> str:
    sessions[session_id] = []
    return _send(sessions[session_id], "Please introduce yourself and ask for the user's name.")


def chat(session_id: str, text: str) -> str:
    history = sessions.setdefault(session_id, [])
    return _send(history, text)


def clear_session(session_id: str) -> None:
    sessions.pop(session_id, None)
