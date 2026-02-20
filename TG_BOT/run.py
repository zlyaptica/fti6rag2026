import asyncio 
import logging
from config import settings
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from src.handlers.handlers import router

bot = Bot(token=settings.tg_model_apikey)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    logging.basicConfig(level=logging.DEBUG)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
