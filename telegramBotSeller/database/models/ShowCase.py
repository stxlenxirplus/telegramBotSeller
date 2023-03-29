import datetime
import random

from database import base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column, DateTime, Text, ForeignKey, Float


class Category(base.Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, default=random.randint(0, 999999999))
    title = Column(String)
    products = relationship("Product", passive_deletes=True)
    creating_date = Column(DateTime, default=datetime.datetime.utcnow)


class Product(base.Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, default=random.randint(0, 999999999))
    title = Column(String)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String, default=None)
    items = relationship("Item", passive_deletes=True)
    category_id = Column(Integer, ForeignKey("category.id", ondelete='CASCADE'))
    category = relationship('Category', back_populates="products")
    creating_date = Column(DateTime, default=datetime.datetime.utcnow)


class Item(base.Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, default=random.randint(0, 999999999))
    content_type = Column(String, default='text')
    content = Column(String)
    status = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey("product.id", ondelete='CASCADE'))
    product = relationship('Product', back_populates="items")
    creating_date = Column(DateTime, default=datetime.datetime.utcnow)
