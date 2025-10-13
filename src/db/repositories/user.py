from db.models import User

from ._base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session=None):
        super().__init__(User, session)


user_repo = UserRepository()
