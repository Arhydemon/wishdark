# adapters/telegram/routers.py

from aiogram import Dispatcher              # ← вот этот импорт
from adapters.telegram.wishes.create    import router as wishes_create_router
from adapters.telegram.wishes.list      import router as wishes_list_router
from adapters.telegram.wishes.questions import router as wishes_questions_router

def register_routers(dp: Dispatcher):
    dp.include_router(wishes_create_router)
    dp.include_router(wishes_list_router)
    dp.include_router(wishes_questions_router)
    # … остальные роутеры
