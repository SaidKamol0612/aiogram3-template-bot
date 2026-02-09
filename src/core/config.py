import logging
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent


# Custom types
LogLevelType = Literal[
    "debug",  # logging.DEBUG
    "info",  # logging.INFO
    "warning",  # logging.WARNING
    "error",  # logging.ERROR
    "critical",  # logging.CRITICAL
]


class BotSettings(BaseModel):
    token: str = "..."

    @model_validator(mode="after")
    def validate_token(self):
        if self.token is None or self.token == "...":
            raise ValueError("Bot token must be set valid token taken from @BotFather")
        return self


class DataBaseSettings(BaseModel):
    url: str = "..."
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @model_validator(mode="after")
    def validate_url(self):
        if self.url is None or self.url == "...":
            raise ValueError("Database url must be set value")
        return self


class LoggingConfig(BaseModel):
    level: LogLevelType = "info"
    fmt: str = (
        "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )
    date_fmt: str = "%Y-%m-%d %H:%M:%S"

    file: Optional[str] = "bot.log"

    @property
    def level_value(self) -> int:
        return getattr(
            logging,
            self.level.upper(),
            logging.INFO,
        )


class Settings(BaseSettings):
    """
    Application settings.
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="CONFIG__",
        env_file=(
            ".env.template",
            ".env.prod",
            ".env.dev",
        ),
        env_ignore_empty=True,
        env_nested_delimiter="__",
    )

    DEBUG: bool = True

    bot: BotSettings = Field(default_factory=BotSettings)
    db: DataBaseSettings = Field(default_factory=DataBaseSettings)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


settings = Settings()
