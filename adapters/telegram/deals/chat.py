from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from infrastructure.db.repositories.deal import DealRepo
from application.deals.service import DealService
from keyboards.reply import main_kb

router = Router()

class ChatForm(StatesGroup):
    in_chat = State()

# 1) Открыть чат
@router.callback_query(lambda c: c.data and c.data.startswith("deal:chat:"))
async def open_chat(cq: CallbackQuery, state: FSMContext):
    _, _, did = cq.data.split(":")
    deal_id = int(did)
    await state.update_data(deal_id=deal_id)
    await state.set_state(ChatForm.in_chat)
    await cq.message.edit_text("💬 Вы в чате сделки. Пишите сообщения:", reply_markup=None)
    await cq.answer()

# 2) Приём сообщений
@router.message(ChatForm.in_chat)
async def chat_message(msg: Message, state: FSMContext):
    data = await state.get_data()
    deal_id = data["deal_id"]
    sender_id = msg.from_user.id

    # Сохраняем в БД
    svc = DealService()
    chat_msg = await svc.send_message(deal_id, sender_id, msg.text)

    # TODO: форвард заказчику/исполнителю (можно запоминать chat_id)
    await msg.answer("✅ Сообщение отправлено.")
