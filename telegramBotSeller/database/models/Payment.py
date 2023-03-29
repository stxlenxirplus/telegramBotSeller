import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float
from database import base

class Payment(base.Base):
    __tablename__ = "payments"
    id = Column(String, unique=True, primary_key=True)
    public_id = Column(String)
    owner_id = Column(BigInteger)
    amount = Column(Float, default=0)
    status = Column(Integer, default=0)
    creating_date = Column(DateTime, default=datetime.datetime.utcnow)