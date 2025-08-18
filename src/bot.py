from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router as main_router
from utils import BotLoader, get_unsubscribed_chat_links
from core.config import settings
from keyboards.inline import channels_list

dp = Dispatcher(storage=MemoryStorage())


async def start_bot() -> None:
    bot = BotLoader.get_bot(settings.bot.token)
    dp.include_router(main_router)
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    user = message.from_user
    channel_links = await get_unsubscribed_chat_links(user.id, bot)

    start_msg = f"Assalomu alaykum @{user.username}!\n"
    kb = None
    if channel_links:
        start_msg += "Iltimos, botdan foydalanishdan avval shu kanalarga obuna bo'ling"
        kb = channels_list(channel_links)

    await message.answer(text=start_msg, reply_markup=kb)
