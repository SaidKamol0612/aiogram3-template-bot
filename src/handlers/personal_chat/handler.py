from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(
    F.chat.type == "private", F.content_type.in_({"text", "photo", "video", "document"})
)
async def echo(message: Message):
    await message.send_copy(message.chat.id)
