import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from aiogram.filters import CommandStart
from aiogram.types import Message

from app.core.config import settings

from app.db.helper import db_helper

from app.handlers import main_router

dispatcher = Dispatcher()


async def main():
    await db_helper.init_db()

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dispatcher.include_router(main_router)

    await dispatcher.start_polling(bot)


@dispatcher.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user

    start_msg = f"Assalomu alaykum @{user.username}!\n"

    await message.answer(text=start_msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except:
        print("Bot stopped.")
    finally:
        asyncio.run(db_helper.dispose())
