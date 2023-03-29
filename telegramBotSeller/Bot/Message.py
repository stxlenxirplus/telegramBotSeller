from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
import Keyboard
from models.ShowCase import get_all_category
from models.User import User


async def show_catalog(update: Union[types.Message, types.CallbackQuery], state: FSMContext):
    context = "В наличии имеются ▼"
    catalog = [await i.get_ for i in await get_all_category()]
    await state.set_state()
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.get_category(catalog))
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context, reply_markup=Keyboard.get_category(catalog))


async def show_profile(update: Union[types.Message, types.CallbackQuery], state: FSMContext):
    user = User(update.from_user.id)
    user_data = await user.get_information
    context = f"Пользователь {update.from_user.full_name}\n\n" \
              f"🔑 Ваш ID: {update.from_user.id}\n" \
              f"💵 Ваш баланс: {user_data.balance}₽"
    from googletrans import Translator
    translator = Translator()

    context = translator.translate(context).text
    await state.set_state()
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.get_profile())
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context, reply_markup=Keyboard.get_profile())
    print("Я ответил")