import logging
import asyncio
from random import choice
from typing import Optional, Dict

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, ReactionTypeEmoji, BotCommand

from core.config import settings

from .states.bot_state import BotState
from .handlers import router as main_router


class BotLoader:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.bot: Optional[Bot] = None
        self.token: Optional[str] = None

    async def init_bot(
        self,
        *,
        bot: Optional[Bot] = None,
        token: Optional[str] = None,
        parse_mode: Optional[ParseMode] = None,
    ):
        if not bot and not token:
            raise ValueError("Either bot or token must be provided")

        async with self.lock:
            if self.bot is None:
                self.token = token
                self.bot = Bot(
                    token=token,
                    default=DefaultBotProperties(
                        parse_mode=parse_mode,
                    ),
                )
        return self.bot

    async def set_bot_commands(self, commands: Dict[str, str]) -> None:
        commands = [BotCommand(command=c, description=d) for c, d in commands.items()]
        await self.bot.set_my_commands(commands)

    async def get_bot(self) -> Bot:
        if self.bot is None:
            raise RuntimeError("Bot is not initialized. Call init_bot(token) first.")
        return self.bot

    async def close_bot(self) -> None:
        if self.bot:
            await self.bot.session.close()
            self.bot = None
            self.token = None


log = logging.getLogger(__name__)
dp = Dispatcher(storage=MemoryStorage())
bot_loader = BotLoader()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    emojies = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🎉", "🤩", "👌", "😍"]
    await message.react([ReactionTypeEmoji(emoji=choice(emojies))])

    user = message.from_user
    user_link = f"tg://user?id={user.id}"

    log.info("%s started bot", user.first_name or user.username)
    start_msg = (
        f"👋 Assalomu alaykum <a href='{user_link}'>"
        f"{user.first_name}</a>, botimizga xush kelibsiz!\n\n"
    )

    await state.set_state(BotState.START)
    await message.reply(text=start_msg)


async def main() -> None:
    bot = await bot_loader.init_bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    dp.include_router(main_router)

    await bot_loader.set_bot_commands({"start": "Launch a bot", "help": "Get help"})
    await dp.start_polling(bot)
