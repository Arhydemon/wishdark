from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List
from domain.models import Wish

def build_wish_list(wishes: List[Wish], page: int = 0, per_page: int = 5):
    builder = InlineKeyboardBuilder()

    # 1) Кнопки-карточки заявок
    for w in wishes:
        text = (
            f"📌 #{w.id} {w.description[:30]}…\n"
            f"💰 {w.amount} {w.currency}  ⏳ {w.deadline}"
        )
        builder.button(text=text, callback_data=f"wish:show:{w.id}")

    # 2) Пагинация и возврат
    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=f"wish:list:{page-1}")
    builder.button(text="❌ Выйти", callback_data="wish:back")
    if len(wishes) == per_page:
        builder.button(text="➡️ Вперёд", callback_data=f"wish:list:{page+1}")

    # 3) Рядность: 1 кнопка для заявок, 2 — для навигации
    builder.adjust(1, 2)
    return builder.as_markup()
