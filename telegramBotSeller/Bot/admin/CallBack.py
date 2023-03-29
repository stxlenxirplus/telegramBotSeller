from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import Keyboard.admin as Keyboard
import Tools
from models.ShowCase import Category, Product, get_all_category


async def get_category(update: Union[types.CallbackQuery, types.Message], state: FSMContext):
    context = "Текущие категории ▼"
    category = await get_all_category()
    raw_category = [await item.get_ for item in category]
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.get_category(raw_category))
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context, reply_markup=Keyboard.get_category(raw_category))


async def create_category(callback: types.CallbackQuery, state: FSMContext):
    context = "Введите название новой категории:"
    await callback.message.edit_text(text=context, reply_markup=Keyboard.get_back())
    await state.set_state("WaitInputTitleNewCategory")


async def open_category(update: Union[types.CallbackQuery, types.Message], state: FSMContext):
    data = Tools.serialize(update.data)
    category = Category(data.get('category_id'))
    category_data = await category.get_
    context = f"[{category_data.title}] Настройки ▼"
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.get_inside_category(category_data.id))
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context, reply_markup=Keyboard.get_inside_category(category_data.id))


async def get_product(update: Union[types.CallbackQuery, types.Message], state: FSMContext):
    data = Tools.serialize(update.data)
    category = Category(data.get('category_id'))
    category_data = await category.get_
    products = await category.products
    context = f"[{category_data.title}] Товары ▼"
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.get_product(products, category.category_id))
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context, reply_markup=Keyboard.get_product(products, category.category_id))


async def create_product(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    context = "Введите название новго продукта:"
    await callback.message.edit_text(text=context, reply_markup=Keyboard.get_back())
    await state.update_data({"category_id": data.get('category_id')})
    await state.set_state("WaitInputTitleNewProduct")


async def edit_title_category(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    context = "Введите новое название категории:"
    await state.update_data({"category_id": data.get('category_id')})
    await state.set_state("WaitInputEditTitleCategory")
    await callback.message.edit_text(context, reply_markup=Keyboard.get_back())


async def delete_category(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    category = Category(data.get('category_id'))
    context = "Успешно"
    await category.delete_()
    await callback.answer(context)
    await get_category(callback, state)


async def open_product(update: Union[types.CallbackQuery, types.Message], state: FSMContext):
    data = Tools.serialize(update.data)
    product = Product(data.get('product_id'))
    product_data = await product.get_
    product_item = await product.items
    activity_item = [item for item in product_item if item.status == 0]
    un_activity_item = [item for item in product_item if item.status == -1]
    context = f"[{product_data.title}] Выберите действие ▼\n" \
              f"Наличие: {len(activity_item)}\n" \
              f"Продано: {len(un_activity_item)}"
    context += "\nФото: 🖼" if product_data.image else "\nФото: 🚫"
    if isinstance(update, types.Message):
        await update.answer(context, reply_markup=Keyboard.open_product(product_data.id, product_data.category_id))
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(context,
                                       reply_markup=Keyboard.open_product(product_data.id, product_data.category_id))


async def add_item(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    markup = Keyboard.choose_content_type().add(InlineKeyboardButton(text="Назад", callback_data="AShowAdminPanel"))
    context = f"[{data.get('product_id')}] Выберите тип товара"
    await state.update_data({"product_id": data.get('product_id')})
    await callback.message.edit_text(context, reply_markup=markup)

async def set_image(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    context = f"[{data.get('product_id')}] Загрузите изображение"
    await state.update_data({"product_id": data.get('product_id')})
    await state.set_state('WaitUploadImageItem')
    await callback.message.edit_text(context, reply_markup=Keyboard.get_back())

async def delete_product(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    product = Product(data.get('product_id'))
    product_data = await product.get_
    callback.data = f"AShowProduct&category_id={product_data.category_id}"
    context = "Успешно"
    await product.delete_()
    await callback.answer(context)
    await get_product(callback, state)


async def choose_content_type(callback: types.CallbackQuery, state: FSMContext):
    data_call = Tools.serialize(callback.data)
    data = await state.get_data()
    context = f"[{data.get('product_id')}] Загрузити товар({data_call.get('content_type')}):"
    await state.update_data({"content_type": data_call.get('content_type')})
    await callback.message.edit_text(context, reply_markup=Keyboard.get_back())
    if data_call.get('content_type') == "file":
        await state.set_state('WaitUploadFileItem')
    if data_call.get('content_type') == "text":
        await state.set_state('WaitUploadTextItem')
