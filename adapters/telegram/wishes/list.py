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
    await state.clear()
    svc = WishService(WishRepo())
    wishes = await svc.list_open_wishes(limit=5, offset=0)
    await msg.answer("Открытые заявки:", reply_markup=build_wish_list(wishes, page=0))

@router.callback_query(lambda c: c.data and c.data.startswith("wish:list:"))
async def cb_list_page(cq: CallbackQuery):
    _, _, page_str = cq.data.split(":")
    wishes = await WishService(WishRepo()).list_open_wishes(limit=5, offset=int(page_str)*5)
    await cq.message.edit_text("Открытые заявки:", reply_markup=build_wish_list(wishes, page=int(page_str)))
    await cq.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("wish:show:"))
async def cb_show_wish(cq: CallbackQuery):
    wish_id = int(cq.data.split(":")[2])
    wish = await WishService(WishRepo()).wish_repo.get_by_id(wish_id)

    text = (
        f"📌 Заявка #{wish.id}\n"
        f"Категория: {wish.id_category}\n"
        f"{wish.description}\n\n"
        f"💰 {wish.amount} {wish.currency}\n"
        f"⏳ {wish.deadline}\n"
        f"Автор: {wish.id_requester}"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="🛠 Взять заявку", callback_data=f"wish:take:{wish.id}")
    kb.button(text="⬅️ Назад",       callback_data="wish:list:0")
    kb.button(text="❓ Вопрос",       callback_data=f"wish:ask:{wish.id}")
    kb.adjust(2, 1)
    await cq.message.edit_text(text, reply_markup=kb.as_markup())
    await cq.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("wish:take:"))
async def cb_take_wish(cq: CallbackQuery):
    # регистрируем/обновляем user и берём внутренний id
    user = await UserRepo().upsert(
        telegram_id=cq.from_user.id,
        username=cq.from_user.username or ""
    )
    wish_id = int(cq.data.split(":")[2])
    try:
        deal = await WishService(WishRepo()).take_wish(wish_id, user.id)
    except Exception as e:
        return await cq.answer(str(e), show_alert=True)

    text = (
        f"✅ Заявка #{wish_id} взята!\n"
        f"ID сделки: {deal.id}\n\n"
        "Нажмите «💬 Открыть чат», чтобы начать общение."
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Открыть чат", callback_data=f"deal:chat:{deal.id}")
    kb.adjust(1)
    await cq.message.edit_text(text, reply_markup=kb.as_markup())
    await cq.answer()
