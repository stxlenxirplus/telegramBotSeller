import base64
import random
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

import Keyboard
import Tools
import config
from models.Payment import Payment
from models.ShowCase import Category, Item, Product
from models.User import User
from models.Payment import check_payment


async def open_category(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    category = Category(data.get('category_id'))
    category_data = await category.get_
    context = f"📃 Категория: {category_data.title}"
    products = await category.products
    reform_products = []
    for product in products:
        object_product = Product(product.id)
        product.items_ = await object_product.items
        reform_products.append(product)

    try:
        await callback.message.edit_text(context, reply_markup=Keyboard.get_product(reform_products))
    except:
        await callback.message.delete()
        await callback.message.answer(context, reply_markup=Keyboard.get_product(reform_products))


async def open_product(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    product = Product(data.get('product_id'))
    product_data = await product.get_
    product_items = await product.items
    user = User(callback.from_user.id)
    user_data = await user.get_information
    context = f"📃 Товар: {product_data.title}\n" \
              f"💰 Цена: {product_data.price}₽\n\n" \
              f"{product_data.description}"
    have_money = user_data.balance >= product_data.price
    activity_product = [item for item in product_items if item.status == 0]
    markup = Keyboard.open_product(product_data.id, product_data.category_id, have_money, activity_product)
    if product_data.image:
        await callback.message.delete()
        await callback.message.answer_photo(photo=product_data.image, caption=context, reply_markup=markup)
    else:
        await callback.message.edit_text(context, reply_markup=markup)


async def not_have_product(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Товар закончился")


async def buy_product(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    product = Product(data.get('product_id'))
    product_data = await product.get_
    product_items = [item for item in await product.items if item.status == 0]
    user = User(callback.from_user.id)
    user_data = await user.get_information
    if user_data.balance < product_data.price:
        await callback.answer("У вас недостаточно средств")
        return

    buy_item = random.choice(product_items)
    object_item = Item(buy_item.id)
    object_item_data = await object_item.get_
    await object_item.update_(status=-1)
    await user.update_data(balance=user_data.balance - product_data.price)
    await callback.message.delete()
    if object_item_data.content_type == "text":
        await callback.message.answer("Спасибо за покупку!\n\n"
                                      f"{object_item_data.content}")
    if object_item_data.content_type == "file":
        await callback.message.answer_document(document=object_item_data.content, caption="Спасибо за покупку!")

    context = f"✅ [{product_data.title}] Новая покупка!\n\n" \
              f"Пользователь: @{callback.from_user.username} | {callback.from_user.id}\n" \
              f"Цена: {product_data.price}\n" \
              f"Тип товара: {object_item_data.content_type}\n" \
              f"Выданный товар:\n" \
              f"{object_item_data.content}"
    for admin in config.admin:
        await callback.bot.send_message(chat_id=admin, text=context)
async def refill_balance(callback: types.CallbackQuery, state: FSMContext):
    context = "Укажите сумму пополнения в рублях:"
    await callback.message.edit_text(context, reply_markup=Keyboard.go_back_profile())
    await state.set_state("WaitInputAmountRefill")


async def check_payment_(callback: types.CallbackQuery, state: FSMContext):
    data = Tools.serialize(callback.data)
    payment = Payment(data.get('payment_id'), callback.from_user.id, 0)
    response, amount = await check_payment(payment.public_id)
    status = await payment.get_status()
    if response and status is not None and status != 1:
        user = User(callback.from_user.id)
        user_data = await user.get_information
        await payment.edit_status(1)
        await callback.message.edit_text("Средстава зачислены на баланс")
        await user.update_data(balance=user_data.balance + amount)
    else:
        await callback.answer("Оплата не найдена")


async def ping(callback: types.CallbackQuery, state: FSMContext):
    print(f"CallBack: {callback.data} | State: {await state.get_data()}")
    await callback.answer(f"CallBack: {callback.data} | State: {await state.get_data()}")
