# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from settings import settings
from di import Container
from infrastructure.db.repo_base import DBSessionMiddleware
from adapters.telegram.routers import register_routers

async def main():
    # 1) Инициализируем пул
    await Container.init()
    pool = Container.pool()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")  # ← так задаём parse_mode
    )
    dp = Dispatcher()

    # 3) Вешаем middleware для БД
    dp.message.middleware(DBSessionMiddleware(pool))
    dp.callback_query.middleware(DBSessionMiddleware(pool))

    # 4) Регистрируем все роутеры
    register_routers(dp)

    # 5) Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
