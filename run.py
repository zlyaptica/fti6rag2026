import os
import logging
import argparse
import sys
import asyncio
import requests

from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from db import chromadb_client
from llm import llm_client


parser = argparse.ArgumentParser(description="RAG-бот телеграмм")
parser.add_argument('--use-webhook', type=bool, default=False, help='Использовать webhook для работы бота')
args = parser.parse_args()

load_dotenv(".env.local")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_POST")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

router = Router()

available_commans = f"""
  Доступные команды:
    /add - добавить факт в базу знаний
    /get_all - список фактов из базы знаний
    /generate - генерация текста только на знаниях LLM
    /search - поиск по базе c форматированием ответа LLM
    /help - доступные команды
"""

help_keyboard = ReplyKeyboardMarkup(
  keyboard = [
    [KeyboardButton(text="/help")]
  ],
  resize_keyboard=True
)

class AddingInDB(StatesGroup):
  entering_text = State()
  llm_generate = State()
  search_fact = State()

@router.message(CommandStart())
async def command_start_handler(message: Message):
  await message.answer(f"""
    Привет! Напиши что-нибудь, и я найду в базе что-нибудь подходящее.
    {available_commans}
  """, reply_markup=help_keyboard)

@router.message(StateFilter(None), Command("add"))
async def command_add_fact_handler(message: Message, state: FSMContext):
  await message.answer(text="Введите текст, который хотите добавить в базу знаний:")
  await state.set_state(AddingInDB.entering_text)

@router.message(Command("get_all"))
async def command_get_facts_handler(message: Message):
  facts = chromadb_client.get_facts()
  await message.answer(text=f"В базу добавлено: {facts}", reply_markup=help_keyboard)

@router.message(StateFilter(None), Command("generate"))
async def command_generate_answer_handler(message: Message, state: FSMContext):
  await message.answer(text="Введите текст, ответ на который будет сгенерирован на основании знаний LLM: ")
  await state.set_state(AddingInDB.llm_generate)

@router.message(StateFilter(None), Command("search"))
async def command_find_fact_handler(message: Message, state: FSMContext):
  await message.answer(text="Что хотите найти?")
  await state.set_state(AddingInDB.search_fact)

@router.message(StateFilter(None), Command("help"))
async def get_help(message: Message, state: FSMContext):
  await message.answer(available_commans, reply_markup=help_keyboard)
  await state.clear()

@router.message(AddingInDB.entering_text)
async def handle_new_text(message: Message, state: FSMContext):
  await state.update_data(entering_text=message.text)
  processing_message = await message.answer("Обрабатываем ваш текст...")

  result = chromadb_client.insert_query(message.text)  
  print(f"{message.from_user.id} добавил {message.text}")

  await processing_message.delete()
  await message.answer("Запись добавлена!", reply_markup=help_keyboard)
  await state.clear()

@router.message(AddingInDB.llm_generate)
async def handle_llm_generating(message: Message, state: FSMContext):
  await state.update_data(llm_generate=message.text)
  processing_message = await message.answer("Генерируем ответ...")

  answer = llm_client.generate_llm_answer(message.text)

  await processing_message.delete()
  await message.answer(answer, reply_markup=help_keyboard)
  await state.clear()

@router.message(AddingInDB.search_fact)
async def handle_llm_generating(message: Message, state: FSMContext):
  await state.update_data(search_fact=message.text)
  processing_message = await message.answer("Ищем ответ...")

  fact = chromadb_client.select_query(message.text)
  llm_answer = llm_client.db_answer_enhance(message.text, fact)

  await processing_message.delete()
  await message.answer(llm_answer, reply_markup=help_keyboard)
  await state.clear()

async def on_startup(bot):
  await bot.set_webhook(WEBHOOK_URL)
  result = await bot.get_webhook_info()

async def on_shutdown(bot):
  await bot.delete_webhook()

async def main():
  dp = Dispatcher()
  dp.include_router(router)
  bot = Bot(TG_BOT_TOKEN)

  if args.use_webhook:
    dp.startup.register(on_startup)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
      dispatcher=dp,
      bot=bot,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host='0.0.0.0', port=int(os.getenv("APP_PORT", 8080)))
  else:
    await dp.start_polling(bot)

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
