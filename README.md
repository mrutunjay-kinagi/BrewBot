# BrewBot ☕

A specialty coffee chat assistant built for [**@mrutunjay.kinagi**](https://www.instagram.com/mrutunjay.kinagi/) — a web-based AI barista that helps people brew better coffee at home.

Live at your Instagram bio link, powered by Groq (Llama 3.3 70B).

---

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
- **Deployment** — Railway

## Local setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/coffee-bot.git
cd coffee-bot

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from console.groq.com

# 5. Run
uvicorn server:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo
4. Add environment variable: `GROQ_API_KEY=your_key_here`
5. Railway auto-deploys — grab the public URL and add it to your Instagram bio

## Environment variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key from [console.groq.com](https://console.groq.com) |
