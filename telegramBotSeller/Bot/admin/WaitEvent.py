import base64
from pathlib import Path

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext

import Keyboard.admin
import Tools
import config
from models.Payment import Payment
from models.ShowCase import Category, Product, Item
from Bot.admin.CallBack import get_category, get_product, open_category, open_product


async def create_category(message: types.Message, state: FSMContext):
    await Category.create_(message.text)
    await get_category(message, state)
    await state.set_state()


async def create_product(message: types.Message, state: FSMContext):
    context = f"[{message.text}] Введите описание продукта"
    await message.answer(context, reply_markup=Keyboard.admin.get_back())
    await state.update_data({"title": message.text})
    await state.set_state("WaitInputDescriptionNewProduct")


async def input_description_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    context = f"[{data.get('title')}] Введите стоимость продукта(например: 1.23)"
    await message.answer(context, reply_markup=Keyboard.admin.get_back())
    await state.update_data({"description": message.text})
    await state.set_state("WaitInputPriceNewProduct")


async def input_price_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    context = f"[{data.get('title')}] Введите стоимость продукта(например: 1.23)"
    if not Tools.is_number(message.text):
        await message.answer(context, reply_markup=Keyboard.admin.get_back())
        return
    await Product.create_(title=data.get('title'), description=data.get('description'),
                          price=float(message.text), category_id=data.get('category_id'))
    message.data = f"AShowProduct&category_id={data.get('category_id')}"
    await state.set_state()
    await get_product(message, state)

async def edit_title_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = Category(data.get('category_id'))
    message.data = f"AOpenCategory&category_id={data.get('category_id')}"
    await category.update_(title=message.text)
    await open_category(message, state)
    await state.set_state()

async def upload_item(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await Item.create_(data.get('product_id'), content_type="file", content=message.document.file_id)
    message.data = f"AOpenProduct&product_id={data.get('product_id')}"
    await open_product(message, state)
    await state.set_state()

async def upload_item_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await Item.create_(data.get('product_id'), content_type="text", content=message.text)
    message.data = f"AOpenProduct&product_id={data.get('product_id')}"
    await open_product(message, state)
    await state.set_state()

async def upload_image(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = Product(data.get('product_id'))
    await product.update_(image=message.photo[-1].file_id)
    message.data = f"AOpenProduct&product_id={data.get('product_id')}"
    await open_product(message, state)
    await state.set_state()


async def input_amount_refill(message: types.Message, state: FSMContext):
    if not Tools.is_number(message.text):
        context = "Укажите сумму пополнения в рублях:"
        await message.answer(context, reply_markup=Keyboard.go_back_profile())
        return
    payment = Payment(Tools.generate_id(12), message.from_user.id, float(message.text))
    context = "Счет успешно сформирован\n\n" \
              f"ID: {payment.id}\n" \
              f"Сумма: {payment.amount}"
    await message.answer(context, reply_markup=payment.markup)
    await state.set_state()