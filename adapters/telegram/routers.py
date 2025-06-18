from aiogram import Dispatcher

from adapters.telegram.wishes.create    import router as wishes_create_router
from adapters.telegram.wishes.list      import router as wishes_list_router
from adapters.telegram.wishes.questions import router as wishes_questions_router
from adapters.telegram.deals.chat       import router as deal_chat_router  # ← вот он

def register_routers(dp: Dispatcher):
    dp.include_router(wishes_create_router)
    dp.include_router(wishes_list_router)
    dp.include_router(wishes_questions_router)
    dp.include_router(deal_chat_router)  # ← регистрируем роутер чата
