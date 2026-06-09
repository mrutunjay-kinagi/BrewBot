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
# Add NVIDIA_API_KEY from build.nvidia.com

# Run dev server (auto-reloads on save)
uvicorn server:app --reload
```

There are no tests or linter configs in this project.

## Architecture

BrewBot is a single-page coffee assistant chatbot. The stack is minimal by design:

- **`server.py`** — FastAPI app. Exposes three endpoints: `POST /api/chat` (send a message), `POST /api/reset` (new session), and `POST /api/edit` (edit a user message and regenerate response). Manages session cookies (UUID), enforces in-memory rate limiting (20 messages/session/hour via `_rate_store`), and delegates all AI logic to `conversation.py`.
- **`conversation.py`** — Owns the session state (`sessions` dict keyed by session ID). Calls NVIDIA's API (google/gemma-3n-e2b-it) via direct HTTP POST to https://integrate.api.nvidia.com/v1/chat/completions with the system prompt prepended to each request. History is capped at 20 messages by trimming from the front. Functions: `start_session` (reset), `chat` (send message), `edit_message` (edit and regenerate).
- **`prompts.py`** — Contains the single `SYSTEM_PROMPT` string that defines BrewBot's persona, coffee knowledge, ratios, recipe format, scope constraints, and jailbreak guardrails.
- **`static/`** — Vanilla HTML/CSS/JS frontend. No build step, no bundler. Frontend includes edit UI with modal dialog for message editing.

**Session lifecycle:** Browser gets a `session_id` cookie on first chat or reset. All state (history, rate limit timestamps) lives in server memory — restarts clear everything.

**Edit feature:** When a user edits a message, the `/api/edit` endpoint truncates the conversation history to before the edited message, re-sends with the new text, and returns the new response. The frontend removes all messages from that edit point onward and renders the new conversation.

**Deployment:** Render. The `Procfile` sets the start command. Required: `NVIDIA_API_KEY` from https://build.nvidia.com/.

## Key constraints

- BrewBot is intentionally coffee-only. The system prompt's guardrails section defines hard rules — preserve these when editing `prompts.py`.
- Ratios are MJ's specific approach (1:15 hot pour-over, 1:10–1:12 iced, always 1:2 espresso) — don't change these without explicit instruction.
