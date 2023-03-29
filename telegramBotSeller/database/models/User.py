import datetime

from database import base
from sqlalchemy import String, Integer, Column, DateTime, BigInteger


class User(base.Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, unique=True)
    username = Column(String)
    balance = Column(Integer, default=0)
    status = Column(Integer, default=0)
    banned = Column(Integer, default=0)
    joining_date = Column(DateTime, default=datetime.datetime.utcnow)
