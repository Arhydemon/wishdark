# adapters/telegram/common.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from infrastructure.db.repositories.user import UserRepo
from keyboards.reply import main_kb

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: Message):
    # сразу регистрируем пользователя
    await UserRepo().upsert(
        telegram_id=msg.from_user.id,
        username=msg.from_user.username or ""
    )
    await msg.answer("Привет! Добро пожаловать в WishDark.", reply_markup=main_kb)
