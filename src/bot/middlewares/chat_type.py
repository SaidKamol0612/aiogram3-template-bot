from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message


class PrivateChatOnlyMiddleware(BaseMiddleware):
    """
    Middleware to restrict command usage to private chats only.
    Sends a warning message if the command is used in a group or channel.
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type != "private":
            await event.answer("⚠️ Bu buyruq faqat shaxsiy suhbatda ishlaydi.")
            return
        return await handler(event, data)


class GroupChannelChatOnlyMiddleware(BaseMiddleware):
    """
    Middleware to restrict command usage to groups, supergroups, or channels.
    Sends a warning message if the command is used in a private chat.
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type not in ("group", "supergroup", "channel"):
            await event.answer("⚠️ Bu buyruq faqat guruhlarda ishlaydi.")
            return
        return await handler(event, data)
