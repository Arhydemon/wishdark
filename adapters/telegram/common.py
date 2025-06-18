# adapters/telegram/common.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from infrastructure.db.repositories.user import UserRepo
from keyboards.reply import main_kb, wishes_kb
# если у тебя ещё нет profile_kb — можешь просто вернуть main_kb после профиля

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: Message):
    # upsert-пользователь
    await UserRepo().upsert(
        telegram_id=msg.from_user.id,
        username=msg.from_user.username or ""
    )
    await msg.answer(
        "Привет! Добро пожаловать в WishDark.",
        reply_markup=main_kb
    )

@router.message(lambda m: m.text == "📂 Заявки")
async def cmd_wishes(msg: Message):
    # показываем меню заявок
    await msg.answer(
        "Выбери раздел заявок:",
        reply_markup=wishes_kb
    )

@router.message(lambda m: m.text == "👤 Профиль")
async def cmd_profile(msg: Message):
    # достаём данные из БД
    user = await UserRepo().get_by_telegram_id(msg.from_user.id)
    text = (
        f"👤 Профиль\n\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"Карма: {user.karma_level}\n"
        f"Статус: {user.account_status}"
    )
    await msg.answer(text, reply_markup=main_kb)
