import sys
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import TG_TOKEN
from app.handlers.user import router as user_router
from app.handlers.admin import router as admin_router
from app.chat.communication import router as chat_router
from app.database.models import async_main

async def main():
    await async_main()
    bot = Bot(token=TG_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(chat_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as error:
        print("Exit - ", error)