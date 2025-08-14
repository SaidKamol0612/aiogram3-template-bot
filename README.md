# Template for Aiogram3 (aiogram 3.0)

This project is a template for quickly building Telegram bots using the **aiogram 3.0** framework. It provides a ready-made structure that allows developers to get started quickly with handling basic commands, asynchronous tasks, and interacting with the Telegram API.

## Features:
- Powered by **aiogram 3.0** for modern async Telegram bot developmert.
- Pre-configured basic commands and handlers to get started quickly.
- Clean, modular structure - easy to extend with custom features.
- Supports inline buttons, callbacks, and rich message handling.
- Optional database integration for storing and managing user data.

## 🚀 Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SaidKamol0612/Template-Aiogram3-Bot.git
   ```

2. **Create and activate `venv`:**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables to `env` file:**

   ```bash
   # Bot configurations
   BOT__BOT__TOKEN=""

   # Database configurations
   BOT__DB__URL="sqlite+aiosqlite:///db.sqlite3"
   ```

5. **Run the server:**

   ```bash
   # .\venv\Scripts\activate
   .\run.bat # for Windows

   # or
   cd src
   python run.py
   ```

---

## 🔓 License and Contribution

This project is open and free to extend, suitable for both beginners and experienced developers who want to quickly set up a Telegram bot and focus on building its functionality. You may use it in commercial or personal projects with minimal restrictions — attribution is appreciated but not required.

> 💡 Contributions and forks are welcome!
