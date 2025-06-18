# adapters/telegram/routers.py

from aiogram import Dispatcher

from adapters.telegram.wishes.create import router as wishes_create_router
from adapters.telegram.wishes.list   import router as wishes_list_router
# позже: from adapters.telegram.deals    import router as deals_router
#         from adapters.telegram.chat     import router as chat_router
#         etc.

def register_routers(dp: Dispatcher):
    dp.include_router(wishes_create_router)
    dp.include_router(wishes_list_router)
    # dp.include_router(deals_router)
    # dp.include_router(chat_router)
    # ...
