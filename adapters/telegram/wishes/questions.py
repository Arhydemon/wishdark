from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from infrastructure.db.repositories.wish import WishRepo
from application.wishes.service import WishService
from keyboards.reply import main_kb

router = Router()

class QForm(StatesGroup):
    waiting_question = State()

@router.callback_query(lambda c: c.data and c.data.startswith("wish:ask:"))
async def ask_start(cq: CallbackQuery, state: FSMContext):
    _, _, wid_str = cq.data.split(":")
    wish_id = int(wid_str)
    await state.update_data(wish_id=wish_id)
    await state.set_state(QForm.waiting_question)
    await cq.message.edit_text(
        "✏️ Напиши свой вопрос заказчику:",
        reply_markup=None
    )
    await cq.answer()

@router.message(QForm.waiting_question)
async def ask_submit(msg: Message, state: FSMContext):
    data = await state.get_data()
    wish_id = data["wish_id"]
    sender_id = msg.from_user.id
    # Узнаем, кто автор заявки
    wish = await WishRepo().get_by_id(wish_id)
    if not wish:
        await msg.answer("❌ Заявка не найдена.", reply_markup=main_kb)
        return await state.clear()

    receiver_id = wish.id_requester
    question_text = msg.text[:300]
    svc = WishService(
        WishRepo(),
        question_repo=None  # будет инициализирован внутри
    )
    try:
        await svc.ask_question(
            wish_id=wish_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            question=question_text
        )
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {e}", reply_markup=main_kb)
        return await state.clear()

    await msg.answer("✅ Вопрос отправлен!", reply_markup=main_kb)
    await state.clear()
