# adapters/telegram/common.py

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from infrastructure.db.repositories.user import UserRepo
from keyboards.reply import main_kb

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: Message):
    # 1) Убеждаемся, что пользователь есть в БД
    await UserRepo().upsert(
        telegram_id=msg.from_user.id,
        username=msg.from_user.username or ""
    )

    # 2) Отправляем приветствие
    await msg.answer(
        "Привет! Добро пожаловать в WishDark.",
        reply_markup=main_kb
    )