from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

from ._base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Optional[AsyncSession] = None):
        super().__init__(User, session)


user_repo = UserRepository()
