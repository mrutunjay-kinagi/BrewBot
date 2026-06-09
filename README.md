# BrewBot ☕

A specialty coffee chat assistant built for [**@mrutunjay.kinagi**](https://www.instagram.com/mrutunjay.kinagi/) — a web-based AI barista that helps people brew better coffee at home.

Powered by NVIDIA's OpenAI-compatible API on build.nvidia.com.

## What it does

- Guides users through brewing recipes for V60, AeroPress, Espresso, French Press, Moka Pot, Cold Brew and more
- Asks the right questions (brew method, hot or iced, number of cups) before giving a recipe
- Follows MJ's approach to ratios — 1:15 for hot pour-over, 1:10–1:12 for iced, always 1:2 for espresso
- Troubleshoots common problems (too bitter, too sour, weak, astringent)
- Stays strictly on-topic — coffee and coffee beverages only
- Prompt injection and jailbreak protection built in

## Stack

- **Backend** — Python, FastAPI, Uvicorn
- **AI** — NVIDIA NIM (google/gemma-3n-e2b-it) via direct HTTP to build.nvidia.com
- **Frontend** — Vanilla HTML/CSS/JS, no framework
- **Deployment** — Render

## Local setup

```bash
git clone https://github.com/YOUR_USERNAME/coffee-bot.git
cd coffee-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your NVIDIA_API_KEY from build.nvidia.com
uvicorn server:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

## Environment variables

| Variable | Description |
|---|---|
| `NVIDIA_API_KEY` | API key from [build.nvidia.com](https://build.nvidia.com/) |
| `NVIDIA_MODEL` | Optional model slug, default `google/gemma-3n-e2b-it` |
| `NVIDIA_BASE_URL` | Optional API base URL, default `https://integrate.api.nvidia.com/v1` |
