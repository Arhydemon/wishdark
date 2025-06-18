from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.reply import main_kb, wishes_kb

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: Message):
    await msg.answer(
        "Привет! Добро пожаловать в WishDark.",
        reply_markup=main_kb
    )

@router.message(lambda m: m.text == "📂 Заявки")
async def open_wishes_menu(msg: Message):
    await msg.answer(
        "Выбери раздел заявок:",
        reply_markup=wishes_kb
    )

@router.message(lambda m: m.text == "⬅️ Назад")
async def back_to_main(msg: Message):
    await msg.answer(
        "Главное меню:",
        reply_markup=main_kb
    )