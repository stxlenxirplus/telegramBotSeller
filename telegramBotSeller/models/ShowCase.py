import types
import typing
from contextlib import closing

import Tools
from database.base import SessionLocal
from database.models.ShowCase import Category as MCategory
from database.models.ShowCase import Product as MProduct
from database.models.ShowCase import Item as MItem


class Category(object):
    def __init__(self, category_id: int = None):
        self.category_id = category_id

    @staticmethod
    async def create_(title: str):
        with closing(SessionLocal()) as db:
            db_record = MCategory(title=title, id=Tools.generate_id_digits(12))
            db.add(db_record), db.commit(), db.refresh(db_record)
            return Category(db_record.id)

    @property
    async def products(self) -> typing.List[MProduct]:
        with closing(SessionLocal()) as db:
            return (db.query(MCategory).filter(MCategory.id == self.category_id).first()).products

    @property
    async def get_(self) -> MCategory:
        with closing(SessionLocal()) as db:
            return db.query(MCategory).filter(MCategory.id == self.category_id).first()

    async def update_(self, **kwargs) -> MCategory:
        with closing(SessionLocal()) as db:
            query = db.query(MCategory).filter(MCategory.id == self.category_id).update(kwargs)
            db.commit()
            return query

    async def delete_(self) -> None:
        with closing(SessionLocal()) as db:
            db.query(MCategory).filter(MCategory.id == self.category_id).delete()
            db.commit()


class Product(object):
    def __init__(self, product_id: int = None):
        self.product_id = product_id

    @staticmethod
    async def create_(title: str, description: str, price: float, category_id: int):
        with closing(SessionLocal()) as db:
            db_record = MProduct(title=title, description=description, price=price, category_id=category_id, id=Tools.generate_id_digits(12))
            db.add(db_record), db.commit(), db.refresh(db_record)
            return Product(db_record.id)

    @property
    async def items(self) -> typing.List[MItem]:
        with closing(SessionLocal()) as db:
            return (db.query(MProduct).filter(MProduct.id == self.product_id).first()).items

    @property
    async def get_(self) -> MProduct:
        with closing(SessionLocal()) as db:
            return db.query(MProduct).filter(MProduct.id == self.product_id).first()

    async def update_(self, **kwargs) -> MProduct:
        with closing(SessionLocal()) as db:
            query = db.query(MProduct).filter(MProduct.id == self.product_id).update(kwargs)
            db.commit()
            return query

    async def delete_(self) -> None:
        with closing(SessionLocal()) as db:
            db.query(MProduct).filter(MProduct.id == self.product_id).delete()
            db.commit()


class Item(object):
    def __init__(self, item_id: int = None):
        self.item_id = item_id

    @staticmethod
    async def create_(product_id: int, content_type: str, content: str = ''):
        with closing(SessionLocal()) as db:
            db_record = MItem(product_id=product_id, content_type=content_type, content=content, id=Tools.generate_id_digits(12))
            db.add(db_record), db.commit(), db.refresh(db_record)
            return Item(db_record.id)

    @property
    async def get_(self) -> MItem:
        with closing(SessionLocal()) as db:
            return db.query(MItem).filter(MItem.id == self.item_id).first()

    async def update_(self, **kwargs) -> MItem:
        with closing(SessionLocal()) as db:
            query = db.query(MItem).filter(MItem.id == self.item_id).update(kwargs)
            db.commit()
            return query

    async def delete_(self) -> None:
        with closing(SessionLocal()) as db:
            db.query(MItem).filter(MItem.id == self.item_id).delete()
            db.commit()


async def get_all_category() -> typing.List[Category]:
    with closing(SessionLocal()) as db:
        query = db.query(MCategory).all()
        return [Category(i.id) for i in query]
