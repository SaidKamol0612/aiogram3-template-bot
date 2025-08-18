__all__ = ("router",)

from aiogram import Router

from middlewares import (
    SubscriptionMiddleware,
    GroupChannelChatOnlyMiddleware,
    PrivateChatOnlyMiddleware,
)

from .public_chat import router as public_router
from .personal_chat import router as personal_router

sub = SubscriptionMiddleware()
router = Router()

public_router.message.middleware(GroupChannelChatOnlyMiddleware())
router.include_router(public_router)

personal_router.message.middleware(PrivateChatOnlyMiddleware())
personal_router.message.middleware(sub)
personal_router.callback_query.middleware(sub)
router.include_router(personal_router)
