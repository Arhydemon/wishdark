# adapters/telegram/menu.py

from aiogram import Router
from aiogram.types import Message
from infrastructure.db.repositories.user import UserRepo
from keyboards.reply import main_kb, wishes_kb

router = Router()

@router.message(lambda m: m.text == "📂 Заявки")
async def cmd_wishes(msg: Message):
    # показать под-меню заявок
    await msg.answer(
        "Выбери раздел заявок:",
        reply_markup=wishes_kb  # reply-клавиатура с “🔍 Открытые”, “🛠 Я исполняю” и т.п.
    )

@router.message(lambda m: m.text == "👤 Профиль")
async def cmd_profile(msg: Message):
    # достаём профиль из БД
    user = await UserRepo().get_by_telegram_id(msg.from_user.id)
    text = (
        f"👤 Ваш профиль:\n\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"Karma: {user.karma_level}\n"
        f"Статус: {user.account_status}\n"
        f"Зарегистрирован: {user.created_at.date()}"
    )
    await msg.answer(text, reply_markup=main_kb)

@router.message(lambda m: m.text == "⬅️ Назад")
async def cmd_back(msg: Message):
    await msg.answer("Вы в главном меню:", reply_markup=main_kb)
