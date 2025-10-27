import logging
from random import choice

from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReactionTypeEmoji

from core.config import settings

from .common.loader import bot_loader
from .handlers import router as main_router
from .states import BotState


log = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    emojies = ["👍", "🔥", "👏", "🎉", "🤩", "👌"]
    await message.react([ReactionTypeEmoji(emoji=choice(emojies))])

    user = message.from_user
    profile_link = f"tg://user?id={user.id}"

    start_msg = (
        f"<b>Salom <a href='{profile_link}'>{user.first_name or '.'}</a>, "
        "botimizga xush kelibsiz!</b>\n\n"
        f"<b>Hello <a href='{profile_link}'>{user.first_name or '.'}</a>, "
        "welcome to our bot!</b>"
    )

    await state.set_state(BotState.START)
    await message.reply(text=start_msg)
    log.info("%s started bot", user.first_name or f"User ({user.id})")


async def main() -> None:
    bot = await bot_loader.init_bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    await bot_loader.set_bot_commands({"start": "Launch a bot", "help": "Get help"})

    dp.include_router(main_router)

    log.info("🚀 Starting polling...")
    await dp.start_polling(bot)
