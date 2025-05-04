from sqlalchemy import BigInteger, String, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)

from app.core import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    tg_id = mapped_column(BigInteger())
    username: Mapped[str] = mapped_column(String())
