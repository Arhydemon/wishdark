from aiogram import Router
from aiogram.types import Message, CallbackQuery
from application.wishes.service import WishService
from infrastructure.db.repositories.wish import WishRepo
from keyboards.inline_wishes import build_wish_list
from keyboards.reply import wishes_kb, main_kb
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(lambda m: m.text == "🔍 Открытые")
async def cmd_list_open(msg: Message):
    svc = WishService(WishRepo())
    wishes = await svc.list_open_wishes(limit=5, offset=0)
    await msg.answer("Открытые заявки:", reply_markup=build_wish_list(wishes, page=0))

@router.callback_query(lambda c: c.data.startswith("wish:list:"))
async def cb_list_page(cq: CallbackQuery):
    _,_,page = cq.data.split(":")
    page = int(page)
    svc = WishService(WishRepo())
    wishes = await svc.list_open_wishes(limit=5, offset=page*5)
    await cq.message.edit_text("Открытые заявки:", reply_markup=build_wish_list(wishes, page))
    await cq.answer()

@router.callback_query(lambda c: c.data.startswith("wish:show:"))
async def cb_show_wish(cq: CallbackQuery):
    _,_,wid = cq.data.split(":")
    wish = await WishService(WishRepo()).wish_repo.get_by_id(int(wid))
    text = (
        f"📌 Заявка #{wish.id}\n"
        f"Категория: {wish.id_category}\n"
        f"{wish.description}\n\n"
        f"💰 {wish.amount} {wish.currency}\n"
        f"⏳ {wish.deadline}\n"
        f"Автор: {wish.id_requester}"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="🛠 Взять заявку", callback_data=f"wish:take:{wish.id}")
    builder.button(text="⬅️ Назад к списку", callback_data="wish:list:0")
    builder.adjust(1, 1)
    await cq.message.edit_text(text, reply_markup=builder.as_markup())
    await cq.answer()

@router.callback_query(lambda c: c.data.startswith("wish:take:"))
async def cb_take_wish(cq: CallbackQuery):
    _,_,wid = cq.data.split(":")
    svc = WishService(WishRepo())
    try:
        await svc.take_wish(int(wid), cq.from_user.id)
    except Exception as e:
        await cq.answer(str(e), show_alert=True)
        return
    await cq.message.edit_text(
        "✅ Заявка взята! Можешь открыть чат по сделке.",
        reply_markup=main_kb
    )
    await cq.answer()
