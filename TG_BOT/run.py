import os
import logging
import asyncio 
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

load_dotenv(".env.local")

tg_token = os.getenv("TG_BOT_APIKEY")
if not tg_token:
    raise ValueError("Токен телеграм бота не найден")

dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def handle_start_message(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Добро пожаловать в бота, который скоро все будет знать! Напиши, что ты хочешь узнать? Напишите запрос и бот напишет все, что знает."
    )

@dp.message(F.text)
async def handle_question(message: Message):
    await message.answer(message.text)

async def main():
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(token=tg_token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
