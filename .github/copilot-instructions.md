# Copilot instructions for BrewBot

## Project shape

BrewBot is a small FastAPI app with a static HTML/CSS/JS frontend and no build step. Keep changes aligned with this split:

- `server.py` handles HTTP routes, the session cookie, and the per-session rate limit.
- `conversation.py` owns in-memory chat history and the NVIDIA API request flow.
- `prompts.py` contains the system prompt; most coffee-domain behavior lives there.
- `static/` is the browser app served directly by FastAPI.

## Commands

```bash
# Set up the local environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure runtime env
cp .env.example .env
# Set NVIDIA_API_KEY in .env

# Run the app locally
uvicorn server:app --reload
```

There is no dedicated test suite or lint configuration in this repository. If you need to verify behavior, use the app directly or run a targeted ad hoc Python check.

## Architecture

- The app is a single-page coffee assistant backed by NVIDIA's OpenAI-compatible API.
- The default model is the free catalog endpoint `google/gemma-3n-e2b-it`; override it with `NVIDIA_MODEL` if needed.
- `/api/chat` continues an existing session; `/api/reset` clears the in-memory session and starts a new one.
- Session state is kept entirely in process memory. A browser session is identified by an `httponly` `session_id` cookie.
- Conversation history is trimmed to the most recent 20 messages.
- The frontend is plain HTML/CSS/JS with no framework or bundler.

## Conventions

- Preserve the coffee-only scope. The assistant should redirect non-coffee requests back to brewing topics.
- Keep MJ’s ratio preferences intact: hot pour-over 1:15, iced pour-over 1:10–1:12, espresso always 1:2.
- Do not replace the system prompt guardrails with looser wording; they are the main defense against prompt injection.
- Keep responses concise and barista-like in tone.
- Treat `NVIDIA_API_KEY` as required. The `.env.example` note about `GEMINI_API_KEY` is stale.
- `PORT` is set by deployment; local development uses `8000` by default.
