import logging
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class BotSettings(BaseModel):
    token: str


class DataBaseSettings(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    log_file: Optional[str] = "bot.log"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="CONFIG__",
        env_file=(BASE_DIR / ".env"),
        env_nested_delimiter="__",
    )

    # NOTE: don't run with debug turned on in production!
    DEBUG: bool = True

    bot: BotSettings
    db: DataBaseSettings
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
