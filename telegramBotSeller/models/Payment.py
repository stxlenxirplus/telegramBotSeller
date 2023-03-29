# -*- coding: utf-8 -*-
import aiohttp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import string
from contextlib import closing
import requests
import config
import database.models.Payment
from database.base import SessionLocal


class Payment(object):

    def __init__(self, id: str, owner_id: int, amount: float):
        self.id = id
        self.owner_id = owner_id
        self.amount = amount

    def __create_payment(self, public_id):
        with closing(SessionLocal()) as db:
            payment = database.models.Payment.Payment(id=self.id, public_id=public_id, owner_id=self.owner_id,
                                                      amount=self.amount)
            db.add(payment)
            db.commit()
            db.refresh(payment)
            return payment

    @property
    def url(self):
        response = requests.get(
            f"https://api.crystalpay.ru/v1/?s={config.secret_key_1_crystal}&n={config.login_crystal}&o=invoice-create&amount={self.amount}&lifetime=60").json()
        self.__create_payment(response['id'])
        return response['url']

    @property
    def public_id(self):
        with closing(SessionLocal()) as db:
            payment = db.query(database.models.Payment.Payment).filter(
                database.models.Payment.Payment.id == self.id).first()
            if payment is not None:
                return payment.public_id

    @property
    def markup(self):
        board = InlineKeyboardMarkup()
        board.add(InlineKeyboardButton(text="Оплатить", url=self.url))
        board.add(InlineKeyboardButton(text="Проверить оплату", callback_data=f"CheckPayment&payment_id={self.id}"))
        return board

    async def edit_status(self, status: int):
        with closing(SessionLocal()) as db:
            payment = db.query(database.models.Payment.Payment).filter(
                database.models.Payment.Payment.id == self.id).update({"status": status})
            db.commit()

    async def get_status(self):
        with closing(SessionLocal()) as db:
            payment = db.query(database.models.Payment.Payment).filter(
                database.models.Payment.Payment.id == self.id).first()
            if payment is not None:
                return payment.status


async def check_payment(public_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://api.crystalpay.ru/v1/?s={config.secret_key_1_crystal}&n={config.login_crystal}&o=invoice-check&i={public_id}")
        response_json = await response.json()
        if not response_json["error"]:
            if response_json["state"] == "payed":
                return True, response_json['amount']
        return False, 0
