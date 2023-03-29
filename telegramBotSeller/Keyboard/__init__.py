# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.models.ShowCase import Category as MCategory
from database.models.ShowCase import Product as MProduct


def get_main() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True). \
        add(KeyboardButton(text="📦 Купить"),
            KeyboardButton(text="🔒Профиль"),
            KeyboardButton(text="🖤 Помощь"))


def get_category(category: list[MCategory]) -> InlineKeyboardMarkup:
    board = InlineKeyboardMarkup()
    for item in category:
        board.add(
            InlineKeyboardButton(text=f"{item.title}", callback_data=f"OpenCategory&category_id={item.id}"))
    return board


def get_product(products: list[MProduct]) -> InlineKeyboardMarkup:
    board = InlineKeyboardMarkup()
    for product in products:
        activity_item = [i for i in product.items_ if i.status == 0]
        current_state = "[Закончился]" if not activity_item else f"[{len(activity_item)}]"
        board.add(InlineKeyboardButton(text=f"{product.title} | {product.price}₽ | {current_state}",
                                       callback_data=f"OpenProduct&product_id={product.id}"))
    return board


def open_product(product_id: int, category_id: int, have_money: bool, allow_buy) -> InlineKeyboardMarkup:
    board = InlineKeyboardMarkup()
    if allow_buy:
        if have_money:
            board.add(InlineKeyboardButton(text="Купить товар", callback_data=f"BuyProduct&product_id={product_id}"))
        else:
            board.add(InlineKeyboardButton(text="У вас недостаточно средств", callback_data="ПЕРЕХОД НА ОПЛАТУ"))
    else:
        board.add(InlineKeyboardButton(text="Товар закончился", callback_data="NotHaveProduct"))
    board.add(InlineKeyboardButton(text="Назад", callback_data=f"OpenCategory&category_id={category_id}"))
    return board

def get_profile():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="➕ Пополнить счёт", callback_data="RefillBalance"))

def go_back_profile():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Назад", callback_data="ShowProfile")
    )