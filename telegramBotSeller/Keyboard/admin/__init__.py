# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models.ShowCase import Category as MCategory
from database.models.ShowCase import Product as MProduct


def get_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="Категории", callback_data="AShowCategory"))


def get_category(category: list[MCategory]) -> InlineKeyboardMarkup:
    board = InlineKeyboardMarkup()
    for item in category:
        board.add(InlineKeyboardButton(text=f"{item.id}: {item.title}", callback_data=f"AOpenCategory&category_id={item.id}"))
    board.add(InlineKeyboardButton(text="Создать новую категорию", callback_data="ACreateNewCategory"))
    board.add(InlineKeyboardButton(text="Назад", callback_data="AShowAdminPanel"))
    return board


def get_inside_category(category_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Открыть товары", callback_data=f"AShowProduct&category_id={category_id}")).add(
        InlineKeyboardButton(text="Изменить название", callback_data=f"AEditCategoryTitle&category_id={category_id}")).add(
        InlineKeyboardButton(text="Удалить категорию", callback_data=f"ADeleteCategory&category_id={category_id}")).add(
        InlineKeyboardButton(text="Назад", callback_data="AShowCategory"))


def get_product(product: list[MProduct], category_id: int) -> InlineKeyboardMarkup:
    board = InlineKeyboardMarkup()
    for item in product:
        board.add(InlineKeyboardButton(text=f"{item.id}: {item.title} | {item.price}", callback_data=f"AOpenProduct&product_id={item.id}"))
    board.add(InlineKeyboardButton(text="Создать новый товар", callback_data=f"ACreateNewProduct&category_id={category_id}"))
    board.add(InlineKeyboardButton(text="Назад", callback_data=f"AOpenCategory&category_id={category_id}"))
    return board

def open_product(product_id: int, category_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Добавить товар", callback_data=f"AAddItemInProduct&product_id={product_id}")).add(
        InlineKeyboardButton(text="Загрузить изображение", callback_data=f"ASetImageProduct&product_id={product_id}")).add(
        InlineKeyboardButton(text="Удалить продукт", callback_data=f"ADeleteProduct&product_id={product_id}")).add(
        InlineKeyboardButton(text="Назад", callback_data=f"AOpenCategory&category_id={category_id}")
    )

def choose_content_type():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Файл', callback_data="ACreateItemChooseContent&content_type=file"),
        InlineKeyboardButton(text='Текстовый', callback_data="ACreateItemChooseContent&content_type=text")
    )

def get_back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="Назад", callback_data="AShowAdminPanel"))
