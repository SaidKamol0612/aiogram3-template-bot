from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdMixin


class User(Base, IntIdMixin):
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_chat_blocked: Mapped[bool] = mapped_column(default=False)
