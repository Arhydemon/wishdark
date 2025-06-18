from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.wish_form import WishForm
from infrastructure.db.repositories.category import CategoryRepo
from infrastructure.db.repositories.wish import WishRepo
from application.wishes.service import WishService
from keyboards.inline import categories_kb, confirm_wish_kb
from keyboards.reply import main_kb, wishes_kb

router = Router()

# 1) старт формы
@router.message(lambda m: m.text == "➕ Новая заявка")
async def start_wish_form(msg: Message, state: FSMContext):
    cats = await CategoryRepo().list_all()
    await state.update_data(categories=cats)
    await state.set_state(WishForm.category)
    kb = categories_kb(cats, page=0)
    await msg.answer("Выбери категорию:", reply_markup=kb)

# 2) листаем страницы категорий
@router.callback_query(lambda c: c.data and c.data.startswith("wish:cat_page"))
async def cat_page(cq: CallbackQuery, state: FSMContext):
    _,_,page_str = cq.data.split(":")
    page = int(page_str)
    data = await state.get_data()
    cats = data["categories"]
    await state.set_state(WishForm.category)
    await cq.message.edit_text("Выбери категорию:", reply_markup=categories_kb(cats, page))
    await cq.answer()

# 3) выбрали категорию
@router.callback_query(lambda c: c.data and c.data.startswith("wish:category"))
async def cat_chosen(cq: CallbackQuery, state: FSMContext):
    _,_,cat_id = cq.data.split(":")
    await state.update_data(category_id=int(cat_id))
    await state.set_state(WishForm.description)
    await cq.message.edit_text("Введи описание (≤1000 знаков):", reply_markup=None)
    await cq.answer()

# 4) описание
@router.message(WishForm.description)
async def set_desc(msg: Message, state: FSMContext):
    text = msg.text[:1000]
    await state.update_data(description=text)
    await state.set_state(WishForm.amount_currency)
    await msg.answer("Введи сумму и валюту (пример: 123.45 USD):")

# 5) сумма+валюта
@router.message(WishForm.amount_currency)
async def set_amount(msg: Message, state: FSMContext):
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.answer("Нужен формат: `<сумма> <валюта>`")
    try:
        amount = float(parts[0])
        currency = parts[1].upper()
    except:
        return await msg.answer("Ошибка в формате, повтори: `100 USD`")
    await state.update_data(amount=amount, currency=currency)
    await state.set_state(WishForm.deadline)
    await msg.answer("Укажи дедлайн YYYY-MM-DD:")

# 6) дедлайн
@router.message(WishForm.deadline)
async def set_deadline(msg: Message, state: FSMContext):
    from datetime import date
    try:
        dl = date.fromisoformat(msg.text)
    except:
        return await msg.answer("Неправильная дата, нужен YYYY-MM-DD")
    await state.update_data(deadline=dl)
    d = await state.get_data()
    txt = (
        f"Проверь, всё верно?\n\n"
        f"Категория: {d['category_id']}\n"
        f"Описание: {d['description']}\n"
        f"Сумма: {d['amount']} {d['currency']}\n"
        f"Дедлайн: {d['deadline']}"
    )
    await state.set_state(WishForm.confirm)
    await msg.answer(txt, reply_markup=confirm_wish_kb())

# 7) подтверждение
@router.callback_query(lambda c: c.data == "wish:confirm")
async def confirm_wish(cq: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    svc = WishService(WishRepo())
    await svc.create_wish(
        user_id=cq.from_user.id,
        id_category=data["category_id"],
        description=data["description"],
        amount=data["amount"],
        currency=data["currency"],
        deadline=data["deadline"]
    )
    await cq.message.edit_text("✅ Заявка создана!", reply_markup=main_kb)
    await state.clear()
    await cq.answer()

# 8) отмена
@router.callback_query(lambda c: c.data == "wish:cancel")
async def cancel_wish(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    await cq.message.edit_text("❌ Создание заявки отменено.", reply_markup=main_kb)
    await cq.answer()
