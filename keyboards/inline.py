# keyboards/inline.py

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from typing import List
from domain.models import Category

def categories_kb(categories: List[Category], page: int = 0, per_page: int = 6):
    # 1) создаём билдер
    builder = InlineKeyboardBuilder()

    # 2) кнопки категорий
    start = page * per_page
    for cat in categories[start : start + per_page]:
        builder.button(text=cat.name, callback_data=f"wish:category:{cat.id}")

    # 3) навигация (2 кнопки в ряд)
    prev_cd = f"wish:cat_page:{page-1}"
    next_cd = f"wish:cat_page:{page+1}"
    # только если есть куда листать
    if page > 0:
        builder.button(text="⬅️", callback_data=prev_cd)
    if len(categories) > start + per_page:
        builder.button(text="➡️", callback_data=next_cd)

    # 4) кнопка отмены в отдельном ряду
    builder.button(text="❌ Отмена", callback_data="wish:cancel")

    # 5) распределяем по рядности:  builder.adjust(cols_per_row)
    builder.adjust(2)  # все кнопки кроме последней “Отмена” — по 2 в ряд

    # 6) возвращаем готовую разметку
    return builder.as_markup()

def confirm_wish_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data="wish:confirm")
    builder.button(text="❌ Отмена",   callback_data="wish:cancel")
    builder.adjust(1)  # одна кнопка в ряд
    return builder.as_markup()
