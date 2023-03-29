from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from models.User import all_users
import Keyboard.admin


async def admin(update: Union[types.Message, types.CallbackQuery], state: FSMContext):
    all_users_ = await all_users()
    context = "Админ панель\n" \
              f"Всего пользователей: {len(all_users_)}"

    await state.set_state()
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.admin.get_main())
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context, reply_markup=Keyboard.admin.get_main())
