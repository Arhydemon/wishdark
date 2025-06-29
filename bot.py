# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from settings import settings
from di import Container
from infrastructure.db.repo_base import DBSessionMiddleware
from adapters.telegram.routers import register_routers

async def main():
    # 1) Поднимаем пул PostgreSQL
    await Container.init()
    pool = Container.pool()

    # 2) Создаём Bot + Dispatcher
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # 3) Middleware для сессии БД
    dp.message.middleware(DBSessionMiddleware(pool))
    dp.callback_query.middleware(DBSessionMiddleware(pool))

    # 4) Регистрируем все роутеры (common, wishes.create, wishes.list, deals.chat…)
    register_routers(dp)

    # 5) Старт polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
