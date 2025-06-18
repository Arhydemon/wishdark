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

# 1) Открыть чат – убрали StateFilter(default=None), просто ловим callback
@router.callback_query(lambda c: c.data and c.data.startswith("deal:chat:"))
async def open_chat(cq: CallbackQuery, state: FSMContext):
    # 1. upsert user
    await UserRepo().upsert(
        telegram_id=cq.from_user.id,
        username=cq.from_user.username or ""
    )
    # 2. подготовка FSM
    await state.clear()
    await state.set_state(ChatForm.in_chat)
    _, _, deal_id_str = cq.data.split(":")
    await state.update_data(deal_id=int(deal_id_str))

    # 3. клавиатура выхода из чата
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 Выйти из чата", callback_data="deal:exit_chat")
    kb.adjust(1)

    await cq.message.edit_text(
        "💬 Вы в чате сделки. Пишите сообщения:",
        reply_markup=kb.as_markup()
    )
    await cq.answer()

# 2) Обработка входящих сообщений только в состоянии in_chat
@router.message(StateFilter(ChatForm.in_chat))
async def chat_receive(msg: Message, state: FSMContext):
    data    = await state.get_data()
    deal_id = data["deal_id"]

    # сохраняем через сервис
    svc = DealService()
    await svc.send_message(deal_id, msg.from_user.id, msg.text)

    # подтверждение
    await msg.answer("✅ Сообщение отправлено.")

# 3) Выход из чата – только из состояния in_chat
@router.callback_query(
    lambda c: c.data == "deal:exit_chat",
    StateFilter(ChatForm.in_chat)
)
async def exit_chat(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    from keyboards.reply import main_kb

    # редактируем старое сообщение и шлём основное меню
    await cq.message.edit_text("🔙 Вы вышли из чата.", reply_markup=None)
    await cq.message.answer("Вы в главном меню:", reply_markup=main_kb)
    await cq.answer()
