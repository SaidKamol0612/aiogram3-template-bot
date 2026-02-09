import logging
from random import choice

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.utils.link import create_tg_link

from core.config import settings

from .handlers import router as main_router
from .states import BotState


log = logging.getLogger(__name__)
EMJIES_FOR_REACTION = ["👍", "🔥", "👏", "🎉", "🤩", "👌"]


async def handle_cmd_start(
    message: Message,
    state: FSMContext,
):
    if message.from_user is None:
        return None

    await message.react(
        [
            ReactionTypeEmoji(
                emoji=choice(EMJIES_FOR_REACTION),
            )
        ]
    )

    user = message.from_user
    log.info(
        "%s [%s] started bot",
        user.first_name or "User",
        user.id,
    )

    user_link = create_tg_link("user", query=f"id={user.id}")
    start_msg = (
        f"<b>Salom <a href='{user_link}'>{user.first_name or '.'}</a>, "
        "botimizga xush kelibsiz!</b>"
    )

    await state.set_state(BotState.START)
    return message.reply(
        text=start_msg,
    )


def create_bot():
    return Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )


def create_dispatcher():
    dispatcher = Dispatcher(
        storage=MemoryStorage(),
    )

    dispatcher.include_router(main_router)
    dispatcher.message.register(handle_cmd_start, CommandStart())

    return dispatcher
