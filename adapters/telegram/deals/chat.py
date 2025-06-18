# adapters/telegram/deals/chat.py

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.deals.service import DealService
from infrastructure.db.repositories.user import UserRepo

router = Router()

class ChatForm(StatesGroup):
    in_chat = State()

@router.callback_query(lambda c: c.data and c.data.startswith("deal:chat:"))
async def open_chat(cq: CallbackQuery, state: FSMContext):
    await UserRepo().upsert(telegram_id=cq.from_user.id, username=cq.from_user.username or "")
    await state.clear()
    await state.set_state(ChatForm.in_chat)
    await state.update_data(deal_id=int(cq.data.split(":")[2]))

    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 Выйти из чата", callback_data="deal:exit_chat")
    kb.adjust(1)
    await cq.message.edit_text("💬 Вы в чате сделки. Пишите сообщения:", reply_markup=kb.as_markup())
    await cq.answer()

@router.message(StateFilter(ChatForm.in_chat))
async def chat_receive(msg: Message, state: FSMContext):
    deal_id = (await state.get_data())["deal_id"]
    await DealService().send_message(deal_id, msg.from_user.id, msg.text)
    await msg.answer("✅ Сообщение отправлено.")

@router.callback_query(lambda c: c.data=="deal:exit_chat", StateFilter(ChatForm.in_chat))
async def exit_chat(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    from keyboards.reply import main_kb
    await cq.message.edit_text("🔙 Вы вышли из чата.", reply_markup=None)
    await cq.message.answer("Вы в главном меню:", reply_markup=main_kb)
    await cq.answer()
