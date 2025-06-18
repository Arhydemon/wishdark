# adapters/telegram/routers.py
from aiogram import Dispatcher
from adapters.telegram.common import router as common_router
from adapters.telegram.wishes.create import router as wishes_create_router
# later: deals, chat, profile, moderator...

from adapters.telegram.wishes.create import router as wishes_create_router

def register_routers(dp: Dispatcher):
    dp.include_router(common_router)
    dp.include_router(wishes_create_router)
    # dp.include_router(deals_router)
    # dp.include_router(chat_router)
    # dp.include_router(profile_router)
    # dp.include_router(moderator_router)
