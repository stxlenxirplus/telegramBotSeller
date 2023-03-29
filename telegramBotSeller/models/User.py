from database.models.User import User as MUser
from typing import Union
from config import aiogramBot
from contextlib import closing
from database.base import SessionLocal


class UserInformation(object):
    def __init__(self, id: int = None, username: str = None, balance: float = 0,
                 status: int = None, banned: int = 0, joining_date: str = None, **kwargs):
        self.id = id
        self.username = username
        self.balance = round(balance, 2)
        self.status = status
        self.banned = banned
        self.joining_date = str(joining_date)

    def __repr__(self):
        return f"{self.id} - {self.username}"


class User(object):
    def __init__(self, user_id: int):
        self.id = user_id

    @property
    async def username(self):
        response = await aiogramBot.get_chat(self.id)
        return response['username']

    @property
    async def is_register(self) -> bool:
        with closing(SessionLocal()) as db:
            db_user = db.query(MUser).filter(MUser.id == self.id).first()
            if db_user is not None:
                return True
        return False

    async def register(self) -> Union[UserInformation, None]:
        with closing(SessionLocal()) as db:
            db_user = MUser(id=self.id, username=await self.username,)
            db.add(db_user), db.commit(), db.refresh(db_user)
            return UserInformation(**db_user.__dict__)

    @property
    async def get_information(self) -> UserInformation:
        with closing(SessionLocal()) as db:
            db_user = db.query(MUser).filter(MUser.id == self.id).first()
        return UserInformation(**db_user.__dict__)

    async def update_data(self, **kwargs):
        with closing(SessionLocal()) as db:
            db.query(MUser).filter(MUser.id == self.id).update(kwargs)
            db_user = db.query(MUser).filter(MUser.id == self.id).first()
            u = UserInformation(**db_user.__dict__), db.commit(), db.close()
            return u

async def all_users():
    with closing(SessionLocal()) as db:
        return db.query(MUser).all()