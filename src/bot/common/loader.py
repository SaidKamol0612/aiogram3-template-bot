from __future__ import annotations

import asyncio
from typing import Optional, Dict

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand


class BotLoader:
    _instance: Optional[BotLoader] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.lock = asyncio.Lock()
            cls._instance.bot = None
            cls._instance.token = None
        return cls._instance

    async def init_bot(
        self,
        *,
        bot: Optional[Bot] = None,
        token: Optional[str] = None,
        parse_mode: Optional[ParseMode] = None,
    ) -> Bot:
        if not bot and not token:
            raise ValueError("Either bot or token must be provided")

        async with self.lock:
            if self.bot is None:
                if bot:
                    self.bot = bot
                    self.token = bot.token
                else:
                    default_props = DefaultBotProperties(
                        parse_mode=parse_mode or ParseMode.HTML
                    )
                    self.bot = Bot(token=token, default=default_props)
                    self.token = token
            else:
                print("⚠️ Bot already initialized. Returning existing instance.")
        return self.bot

    async def set_bot_commands(self, commands: Dict[str, str]) -> None:
        if self.bot is None:
            raise RuntimeError("Bot is not initialized")

        bot_commands = [
            BotCommand(command=c, description=d) for c, d in commands.items()
        ]
        await self.bot.set_my_commands(bot_commands)

    async def get_bot(self) -> Bot:
        if self.bot is None:
            raise RuntimeError("Bot is not initialized. Call init_bot() first.")
        return self.bot

    async def close_bot(self) -> None:
        if self.bot:
            try:
                await self.bot.session.close()
            finally:
                self.bot = None
                self.token = None


bot_loader = BotLoader()
