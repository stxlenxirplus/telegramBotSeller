from aiogram import types
from aiogram.dispatcher import FSMContext

import Keyboard
from models.User import User

async def start(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    if await user.is_register:
        user_data = await user.get_information
        if user_data.banned:return
    else:
        await user.register()
    await message.answer(f"Добро пожаловать {message.from_user.first_name}, в небольшой магазинчик неплохих  логов",
                         reply_markup=Keyboard.get_main())
