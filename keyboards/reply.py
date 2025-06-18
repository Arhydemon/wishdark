from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📂 Заявки"),
            KeyboardButton(text="👤 Профиль")
        ]
    ],
    resize_keyboard=True
)

wishes_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍 Открытые"),
            KeyboardButton(text="📤 Мои заявки")
        ],
        [
            KeyboardButton(text="🛠 Я исполняю"),
            KeyboardButton(text="➕ Новая заявка")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ],
    ],
    resize_keyboard=True
)
