from aiogram.fsm.state import StatesGroup, State

class WishForm(StatesGroup):
    category         = State()  # выбор категории
    description      = State()  # ввод описания
    amount_currency  = State()  # ввод «сумма валюта»
    deadline         = State()  # ввод дедлайна
    confirm          = State()  # подтверждение
