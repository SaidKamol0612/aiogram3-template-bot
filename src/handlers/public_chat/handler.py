import logging

from aiogram import Router, F
from aiogram.types import ChatJoinRequest, Message

from utils.request import RequestUtils

router = Router()
log = logging.getLogger(__name__)


@router.chat_join_request()
async def handle_join_request(event: ChatJoinRequest):
    user_id = event.from_user.id
    channel_id = str(event.chat.id)
    RequestUtils.add_request(user_id, channel_id)
    log.info(f"Add request: user {user_id} → channel {channel_id}")


@router.message(F.text == "/id")
async def get_id(msg: Message):
    await msg.answer(str(msg.chat.id))


@router.channel_post(F.text == "/id")
async def get_id(post: Message):
    await post.answer(str(post.chat.id))
