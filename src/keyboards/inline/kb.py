from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def channels_list(links: List[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for link in links:
        kb.add(
            InlineKeyboardButton(text="✅ Obuna bo'lish", url=link),
        )

    return kb.adjust(1).as_markup()
