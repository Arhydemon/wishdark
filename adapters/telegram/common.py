# adapters/telegram/wishes/list.py

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.wishes.service import WishService
from infrastructure.db.repositories.wish import WishRepo
from infrastructure.db.repositories.user import UserRepo
from keyboards.reply import main_kb
from keyboards.inline_wishes import build_wish_list

router = Router()

@router.message(lambda m: m.text == "🔍 Открытые")
async def cmd_list_open(msg: Message, state: FSMContext):
    # Сбрасываем FSM, если до этого была форма
    await state.clear()
    svc = WishService(WishRepo())
    wishes = await svc.list_open_wishes(limit=5, offset=0)
    await msg.answer(
        "Открытые заявки:",
        reply_markup=build_wish_list(wishes, page=0)
    )

@router.callback_query(lambda c: c.data and c.data.startswith("wish:list:"))
async def cb_list_page(cq: CallbackQuery):
    _, _, page_str = cq.data.split(":")
    page = int(page_str)
    svc = WishService(WishRepo())
    wishes = await svc.list_open_wishes(limit=5, offset=page * 5)
    await cq.message.edit_text(
        "Открытые заявки:",
        reply_markup=build_wish_list(wishes, page=page)
    )
    await cq.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("wish:show:"))
async def cb_show_wish(cq: CallbackQuery):
    _, _, wid_str = cq.data.split(":")
    wish_id = int(wid_str)
    wish = await WishService(WishRepo()).wish_repo.get_by_id(wish_id)

    text = (
        f"📌 Заявка #{wish.id}\n"
        f"Категория: {wish.id_category}\n"
        f"{wish.description}\n\n"
        f"💰 {wish.amount} {wish.currency}\n"
        f"⏳ {wish.deadline}\n"
        f"Автор: {wish.id_requester}"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="🛠 Взять заявку",        callback_data=f"wish:take:{wish.id}")
    builder.button(text="⬅️ Назад к списку",    callback_data="wish:list:0")
    builder.button(text="❓ Задать вопрос",      callback_data=f"wish:ask:{wish.id}")
    builder.adjust(2, 1)

    await cq.message.edit_text(text, reply_markup=builder.as_markup())
    await cq.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("wish:take:"))
async def cb_take_wish(cq: CallbackQuery):
    # 1) upsert пользователя и получаем internal id
    user = await UserRepo().upsert(
        telegram_id=cq.from_user.id,
        username=cq.from_user.username or ""
    )

    # 2) вытаскиваем id заявки
    _, _, wid_str = cq.data.split(":")
    wish_id = int(wid_str)

    svc = WishService(WishRepo())
    try:
        # 3) передаём внутренний user.id
        deal = await svc.take_wish(wish_id, user.id)
    except Exception as e:
        return await cq.answer(str(e), show_alert=True)

    # 4) отправляем сообщение с кнопкой чата
    text = (
        f"✅ Заявка #{wish_id} взята!\n"
        f"ID сделки: {deal.id}\n\n"
        "Нажмите «💬 Открыть чат», чтобы начать общение."
    )
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💬 Открыть чат",
        callback_data=f"deal:chat:{deal.id}"
    )
    builder.adjust(1)

    await cq.message.edit_text(text, reply_markup=builder.as_markup())
    await cq.answer()
