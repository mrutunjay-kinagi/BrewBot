# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy and fill in env vars
cp .env.example .env
# Add GROQ_API_KEY from console.groq.com

# Run dev server (auto-reloads on save)
uvicorn server:app --reload
```

There are no tests or linter configs in this project.

## Architecture

BrewBot is a single-page coffee assistant chatbot. The stack is minimal by design:

- **`server.py`** — FastAPI app. Exposes two endpoints: `POST /api/chat` and `POST /api/reset`. Manages session cookies (UUID), enforces in-memory rate limiting (20 messages/session/hour via `_rate_store`), and delegates all AI logic to `conversation.py`.
- **`conversation.py`** — Owns the session state (`sessions` dict keyed by session ID). Calls the Groq API (Llama 3.3 70B) with the system prompt prepended to each request. History is capped at 20 messages by trimming from the front. `start_session` resets history and sends an introductory prompt; `chat` continues an existing session.
- **`prompts.py`** — Contains the single `SYSTEM_PROMPT` string that defines BrewBot's persona, coffee knowledge, ratios, recipe format, scope constraints, and jailbreak guardrails.
- **`static/`** — Vanilla HTML/CSS/JS frontend. No build step.

**Session lifecycle:** Browser gets a `session_id` cookie on first chat or reset. All state (history, rate limit timestamps) lives in server memory — restarts clear everything.

**Deployment:** Render. The `Procfile` sets the start command. The `.env.example` note about `GEMINI_API_KEY` is a leftover — the actual required key is `GROQ_API_KEY`.

## Key constraints

- BrewBot is intentionally coffee-only. The system prompt's guardrails section defines hard rules — preserve these when editing `prompts.py`.
- Ratios are MJ's specific approach (1:15 hot pour-over, 1:10–1:12 iced, always 1:2 espresso) — don't change these without explicit instruction.
