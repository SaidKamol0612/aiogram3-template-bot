import logging
import asyncio

from bot import main
from core.config import settings
from db import db_helper

log = logging.getLogger(__name__)


async def run_bot():
    await db_helper.init_db()

    try:
        await main()
    except asyncio.CancelledError:
        logging.info("Bot task cancelled. Exiting gracefully...")
    except KeyboardInterrupt:
        logging.info("Bot stopped manually with Ctrl+C.")
    except Exception as e:
        logging.exception("Bot stopped with unexpected exception: %s", e)
    finally:
        await db_helper.dispose()


if __name__ == "__main__":
    logging.basicConfig(
        filename=settings.logging.log_file if not settings.DEBUG else None,
        format=settings.logging.log_format,
        datefmt=settings.logging.log_date_format,
        level=settings.logging.log_level_value,
    )

    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logging.info("Bot stopped manually with Ctrl+C at main level.")
