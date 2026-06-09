import os
from dotenv import load_dotenv
import requests
from prompts import SYSTEM_PROMPT

load_dotenv()

# Use direct HTTP calls to NVIDIA's OpenAI-compatible endpoint (NIM).
MODEL = os.getenv("NVIDIA_MODEL", "google/gemma-3n-e2b-it")

# {session_id: [{"role": "user"|"assistant", "content": str}]}
sessions: dict[str, list[dict]] = {}

MAX_HISTORY = 20


def _send(history: list[dict], text: str) -> str:
    history.append({"role": "user", "content": text})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    # Direct HTTP call to NVIDIA / OpenAI-compatible endpoint
    base = os.environ.get("NVIDIA_BASE_URL") or os.environ.get("OPENAI_API_BASE") or "https://integrate.api.nvidia.com/v1"
    url = base.rstrip("/") + "/chat/completions"
    api_key = os.environ.get("NVIDIA_API_KEY") or os.environ.get("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": float(os.getenv("DEFAULT_TEMPERATURE", 0.2)),
        "top_p": float(os.getenv("DEFAULT_TOP_P", 0.7)),
        "stream": False,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    j = r.json()
    # Support OpenAI-compatible response shapes
    reply = None
    if isinstance(j, dict):
        choices = j.get("choices") or []
        if choices:
            msg = choices[0].get("message") or {}
            reply = msg.get("content") or choices[0].get("text")
    if reply is None:
        reply = str(j)
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
