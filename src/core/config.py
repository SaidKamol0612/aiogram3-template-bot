import logging
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = (BASE_DIR / "db.sqlite3").resolve()

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class BotSettings(BaseModel):
    token: str


class DataBaseSettings(BaseModel):
    class DBURLSetting(BaseModel):
        db_type: str = "sqlite"
        db_driver: str = "aiosqlite"
        db_user: Optional[str] = "user"
        db_pass: Optional[str] = "password"
        db_host: Optional[str] = "localhost"
        db_port: Optional[int] = 5432
        db_name: Optional[str] = "mydb"
        db_path: Optional[Path] = DB_PATH  # for SQLite

        @field_validator("db_path", mode="before")
        def check_required_fields(cls, v, info):
            values = info.data
            db_type = values.get("db_type", "sqlite")
            if db_type == "sqlite" and not v:
                raise ValueError("db_path is required for SQLite")
            return v

        @property
        def db_url(self) -> str:
            if self.db_type == "sqlite":
                return f"{self.db_type}+{self.db_driver}:///{self.db_path}"
            else:
                if not all(
                    [
                        self.db_user,
                        self.db_pass,
                        self.db_host,
                        self.db_port,
                        self.db_name,
                    ]
                ):
                    raise ValueError("Missing required DB connection info")
                return f"{self.db_type}+{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    url: DBURLSetting
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
        return getattr(logging, self.log_level.upper(), logging.INFO)


class Settings(BaseSettings):
    """
    Application settings.
    Loaded from environment variables with prefix `CONFIG__`.
    """

    # NOTE: don't run with debug turned on in production!
    DEBUG: bool = True

    bot: BotSettings
    db: DataBaseSettings
    logging: LoggingConfig = LoggingConfig()

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="CONFIG__",
        env_file=(BASE_DIR / ".env"),
        env_nested_delimiter="__",
    )


settings = Settings()  # type: ignore
