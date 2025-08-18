from typing import Union
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from keyboards.inline import channels_list
from utils.sub_check import get_unsubscribed_chat_links


from typing import Callable, Awaitable, Union
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from utils.sub_check import get_unsubscribed_chat_links
from keyboards.inline import channels_list

class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], dict], Awaitable],
        event: Union[Message, CallbackQuery],
        data: dict
    ):
        bot: Bot = data["bot"]
        user_id = event.from_user.id
        unsubscribed = await get_unsubscribed_chat_links(user_id, bot)

        if unsubscribed:
            text = "Чтобы пользоваться ботом, подпишитесь на каналы:"
            kb = channels_list(unsubscribed)
            if isinstance(event, Message):
                await event.answer(text, reply_markup=kb)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(text, reply_markup=kb)
            return

        return await handler(event, data)

