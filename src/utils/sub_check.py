import logging

from aiogram import Bot

from core import settings

from .request import RequestUtils

log = logging.getLogger(__name__)


async def get_unsubscribed_chat_links(user_id: int, bot: Bot):
    open_links_id, closed_links_id = settings.required_links.links_id
    unsubscribed_chat_links = []

    for username in open_links_id:
        try:
            member = await bot.get_chat_member(username, user_id)
            if member.status not in ("member", "administrator", "creator"):
                unsubscribed_chat_links.append(f"https://t.me/{username.lstrip('@')}")
        except Exception as e:
            log.error(f"Ошибка проверки канала {username}: {e}")
            unsubscribed_chat_links.append(f"https://t.me/{username.lstrip('@')}")

    for chat_id in closed_links_id:
        try:
            member = await bot.get_chat_member(chat_id, user_id)
            request = RequestUtils.has_request(user_id, chat_id)
            if (
                member.status not in ("member", "administrator", "creator")
                and not request
            ):
                link = await bot.create_chat_invite_link(
                    chat_id=chat_id,
                    name="Join via bot approval",
                    creates_join_request=True,
                )
                unsubscribed_chat_links.append(link.invite_link)
        except Exception as e:
            log.error(f"Ошибка проверки канала {chat_id}: {e}")
            try:
                link = await bot.create_chat_invite_link(
                    chat_id=chat_id,
                    name="Join via bot approval",
                    creates_join_request=True,
                )
                unsubscribed_chat_links.append(link.invite_link)
            except Exception as ex:
                log.error(f"Не удалось создать ссылку для {chat_id}: {ex}")

    return unsubscribed_chat_links
