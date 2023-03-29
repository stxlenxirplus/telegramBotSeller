import config
from typing import Union
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class Admin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        return message.from_user.id in config.admin
