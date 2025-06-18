# adapters/telegram/wishes/create.py

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from infrastructure.db.repositories.user     import UserRepo
from infrastructure.db.repositories.category import CategoryRepo
from infrastructure.db.repositories.wish     import WishRepo
from application.wishes.service              import WishService
from keyboards.inline                        import categories_kb, confirm_wish_kb
from keyboards.reply                         import main_kb
from states.wish_form                        import WishForm

router = Router()

# 1) старт формы
@router.message(lambda m: m.text == "➕ Новая заявка")
async def start_wish_form(msg: Message, state: FSMContext):
    cats = await CategoryRepo().list_all()
    await state.set_state(WishForm.category)
    await state.update_data(categories=cats)
    await msg.answer("Выбери категорию:", reply_markup=categories_kb(cats, page=0))

# 2) листаем страницы категорий
@router.callback_query(lambda c: c.data.startswith("wish:cat_page"), StateFilter(WishForm.category))
async def cat_page(cq: CallbackQuery, state: FSMContext):
    _, _, page_str = cq.data.split(":")
    page = int(page_str)
    cats = (await state.get_data())["categories"]
    await cq.message.edit_text("Выбери категорию:", reply_markup=categories_kb(cats, page))
    await cq.answer()

# 3) выбрали категорию
@router.callback_query(lambda c: c.data.startswith("wish:category"), StateFilter(WishForm.category))
async def cat_chosen(cq: CallbackQuery, state: FSMContext):
    _, _, cat_id = cq.data.split(":")
    await state.update_data(category_id=int(cat_id))
    await state.set_state(WishForm.description)
    await cq.message.edit_text("Введи описание (≤1000 знаков):", reply_markup=None)
    await cq.answer()

# 4) описание
@router.message(StateFilter(WishForm.description))
async def set_desc(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text[:1000])
    await state.set_state(WishForm.amount_currency)
    await msg.answer("Введи сумму и валюту (пример: 123.45 USD):")

# 5) сумма + валюта
@router.message(StateFilter(WishForm.amount_currency))
async def set_amount(msg: Message, state: FSMContext):
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.answer("Нужен формат: сумма и валюта (пример: 100 USD).")
    try:
        amount = float(parts[0])
    except ValueError:
        return await msg.answer("Ошибка в формате суммы. Введите число, например: 100")
    currency = parts[1].upper()
    if len(currency) > 5:
        return await msg.answer("Код валюты должен быть не длиннее 5 символов (например: USD).")
    await state.update_data(amount=amount, currency=currency)
    await state.set_state(WishForm.deadline)
    await msg.answer("Укажи дедлайн в формате YYYY-MM-DD:")

# 6) дедлайн
@router.message(StateFilter(WishForm.deadline))
async def set_deadline(msg: Message, state: FSMContext):
    from datetime import date
    try:
        dl = date.fromisoformat(msg.text)
    except ValueError:
        return await msg.answer("Неправильная дата, нужен YYYY-MM-DD")
    await state.update_data(deadline=dl)
    data = await state.get_data()
    txt = (
        f"Проверь, всё верно?\n\n"
        f"Категория: {data['category_id']}\n"
        f"Описание: {data['description']}\n"
        f"Сумма: {data['amount']} {data['currency']}\n"
        f"Дедлайн: {data['deadline']}"
    )
    await state.set_state(WishForm.confirm)
    await msg.answer(txt, reply_markup=confirm_wish_kb())

# 7) подтверждение
@router.callback_query(lambda c: c.data == "wish:confirm", StateFilter(WishForm.confirm))
async def confirm_wish(cq: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if "category_id" not in data:
        await cq.answer("Сессия истекла, начните заново.", show_alert=True)
        await state.clear()
        return

    # upsert-пользователь и внутренний id
    user = await UserRepo().upsert(
        telegram_id=cq.from_user.id,
        username=cq.from_user.username or ""
    )

    # создаём заявку
    svc = WishService(WishRepo())
    await svc.create_wish(
        user_id    = user.id,
        id_category= data["category_id"],
        description= data["description"],
        amount     = data["amount"],
        currency   = data["currency"],
        deadline   = data["deadline"],
    )

    # убираем inline-клавиатуру и сообщаем об успехе
    await cq.message.edit_text("✅ Заявка создана!")
    # отправляем новое сообщение с Reply-клавиатурой
    await cq.message.answer("Вы в главном меню:", reply_markup=main_kb)

    await state.clear()
    await cq.answer()

# 8) отмена
@router.callback_query(lambda c: c.data == "wish:cancel", StateFilter(WishForm))
async def cancel_wish(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    await cq.message.edit_text("❌ Создание заявки отменено.")
    await cq.message.answer("Вы в главном меню:", reply_markup=main_kb)
    await cq.answer()
