import asyncio
import logging

from bot import create_bot, create_dispatcher
from core import settings


async def main() -> None:
    dispatcher = create_dispatcher()
    bot = create_bot()

    await bot.delete_webhook(drop_pending_updates=False)
    await dispatcher.start_polling(bot)


def setup_logging() -> None:
    root = logging.getLogger()

    for h in root.handlers:
        root.removeHandler(h)

    formatter = logging.Formatter(
        fmt=settings.logging.fmt,
        datefmt=settings.logging.date_fmt,
    )

    root.setLevel(settings.logging.level_value)

    sh = logging.StreamHandler()
    sh.setLevel(settings.logging.level_value)
    sh.setFormatter(formatter)
    root.addHandler(sh)

    if not settings.DEBUG and settings.logging.file is not None:
        fh = logging.FileHandler(settings.logging.file)
        fh.setLevel(settings.logging.level_value)
        fh.setFormatter(formatter)
        root.addHandler(fh)

    logging.getLogger("aiogram").setLevel(settings.logging.level_value)
    logging.getLogger("aiogram.dispatcher").setLevel(settings.logging.level_value)
    logging.getLogger("aiogram.event").setLevel(settings.logging.level_value)


if __name__ == "__main__":
    setup_logging()

    asyncio.run(main())
