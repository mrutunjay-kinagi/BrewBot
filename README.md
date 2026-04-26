# BrewBot ☕

A specialty coffee chat assistant built for [**@mrutunjay.kinagi**](https://www.instagram.com/mrutunjay.kinagi/) — a web-based AI barista that helps people brew better coffee at home.

Powered by Groq (Llama 3.3 70B).

## What it does

- Guides users through brewing recipes for V60, AeroPress, Espresso, French Press, Moka Pot, Cold Brew and more
- Asks the right questions (brew method, hot or iced, number of cups) before giving a recipe
- Follows MJ's approach to ratios — 1:15 for hot pour-over, 1:10–1:12 for iced, always 1:2 for espresso
- Troubleshoots common problems (too bitter, too sour, weak, astringent)
- Stays strictly on-topic — coffee and coffee beverages only
- Prompt injection and jailbreak protection built in

## Stack

- **Backend** — Python, FastAPI, Uvicorn
- **AI** — Groq API (Llama 3.3 70B)
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
# Add your GROQ_API_KEY from console.groq.com
uvicorn server:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

## Environment variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key from [console.groq.com](https://console.groq.com) |
