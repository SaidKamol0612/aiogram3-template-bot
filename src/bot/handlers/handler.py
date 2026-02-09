from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.bot_state import BotState


router = Router()


@router.message(F.text, BotState.START)
async def echo(message: Message, state: FSMContext):
    if message.from_user is None:
        return

    return message.send_copy(message.from_user.id)
