# Telegram Bot Template (Aiogram 3)

![Python](https://img.shields.io/badge/python-3.11-blue)
![Aiogram](https://img.shields.io/badge/aiogram-3.0-green)

A scalable **Telegram bot template** built with **Aiogram 3**, featuring:

- Async CRUD with SQLAlchemy 2.x & Pydantic
- FSM (Finite State Machine) for conversation management
- Middleware for private and group chats
- Subscription system with open/closed channels
- Clean project structure ready for production

---

## 📂 Project Structure

```
src/
├─ core/
│  ├─ __init__.py
│  └─ config.py
├─ db/
│  ├─ crud/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ user_crud.py
│  │  └─ subscription_crud.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ user.py
│  │  └─ subscription.py
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  ├─ user_schema.py
│  │  └─ subscription_schema.py
│  ├─ __init__.py
│  └─ helper.py
├─ handlers/
│  ├─ personal/
│  │  ├─ __init__.py
│  │  └─ handler.py
│  └─ __init__.py
├─ keyboards/
│  ├─ inline/
│  │  ├─ __init__.py
│  │  └─ kb.py
│  └─ reply/
│     ├─ __init__.py
│     └─ kb.py
├─ middlewares/
│  ├─ __init__.py
│  └─ chat_type.py
├─ states/
│  ├─ __init__.py
│  └─ bot_state.py
├─ utils/
│  ├─ __init__.py
│  ├─ case_converter.py
│  ├─ load.py
│  ├─ request.py
│  ├─ requests.json
│  └─ sub_check.py
├─ .env            # create and fill
├─ .env.template
├─ bot.log         # creates after run
├─ bot.py
├─ db.sqlite3      # creates after run
└─ run.py
.gitignore
README.md
requirements.txt
run.bat
```

---

## ⚡ Features

- **Async CRUD**
  BaseCRUD supports `create`, `read`, `read_all`, `update`, `delete` with SQLAlchemy + Pydantic schemas.

- **FSM support**
  Handle multi-step conversations easily using Aiogram FSM.

- **Middleware**
  Restrict certain commands to private chats or groups/channels.

- **Subscription system**

  - Open subscriptions: user must be a member
  - Closed subscriptions: bot generates join request links automatically

- **Graceful shutdown**
  Ensures DB sessions and bot polling are properly closed on `Ctrl+C` or exceptions.

---

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/SaidKamol0612/Template-Aiogram3-Bot.git
cd Template-Aiogram3-Bot
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```text
# .env
BOT__BOT__TOKEN=<your_telegram_bot_token>
BOT__DB__URL=sqlite+aiosqlite:///./database.db
```

---

## 🚀 Running the Bot

```bash
run.bat
# or
python src/run.py
```

The bot will initialize the database and start polling.

---

## 📦 Usage

- Add users and subscriptions via CRUD classes (`UserCRUD`, `SubscriptionCRUD`).
- Use FSM for multi-step commands.
- Middleware ensures commands are executed in the correct chat type.
- `get_unsubscribed_chat_links(user_id, bot)` helps manage subscription checks automatically.

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

MIT License © \[Your Name]
