# Aiogram3 template bot

![Python](https://img.shields.io/badge/python-3.11-blue)
![Aiogram](https://img.shields.io/badge/aiogram-3.0-green)

A scalable **Telegram bot template** built with **Aiogram 3**, featuring:

- Async CRUD with SQLAlchemy 2.x & Pydantic
- FSM (Finite State Machine) for conversation management
- Middleware for private and group chats
- Subscription system with open/closed channels
- Clean project structure ready for production

---


## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/SaidKamol0612/aiogram3-template-bot.git
cd aiogram3-template-bot
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

2.1. Install dependencies:

```bash
pip install -r requirements.txt
```


2.2 Or install dependencies via Poetry:

```bash
make build
```

4. Configure environment variables:

Copy `.env.template`:

```bash
cp .env.template .env.dev
```

Fill variables:

```env
BOT__BOT__TOKEN=<your_telegram_bot_token>
BOT__DB__URL=sqlite+aiosqlite:///db.sqlite3
```

---

## 🚀 Running the Bot

```bash
make run
# or
python -m src.main
```

The bot will initialize the database and start polling.

---


## ⚙️ Settings

All settings are located in `core/config.py` using **Pydantic BaseSettings**:

- `BOT__BOT__TOKEN` – Telegram Bot API token
- `BOT__DB__URL` – SQLAlchemy database URL
- Logging configuration is fully customizable

---

## ✅ Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

MIT License © \Mirsaidov Saidkamol
