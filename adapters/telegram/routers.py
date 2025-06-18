# adapters/telegram/routers.py

from aiogram import Dispatcher

from adapters.telegram.common import router as common_router
from adapters.telegram.wishes.create import router as wishes_create_router
from adapters.telegram.wishes.list import router as wishes_list_router
from adapters.telegram.deals.chat import router as deals_chat_router

def register_routers(dp: Dispatcher):
    dp.include_router(common_router)
    dp.include_router(wishes_create_router)
    dp.include_router(wishes_list_router)
    dp.include_router(deals_chat_router)
