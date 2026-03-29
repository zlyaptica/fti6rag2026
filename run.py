import logging
import sys
import asyncio
from aiohttp import web
from flask import Flask, request, jsonify
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import os
from dotenv import load_dotenv
import requests


load_dotenv(".env.local")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_POST")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

router = Router()

class AddingInDB(StatesGroup):
  entering_text = State()

@router.message(CommandStart())
async def command_start_handler(message: Message):
  await message.answer(f"Привет! Напиши что-нибудь, и я найду в базе что-нибудь подходящее. Для добавления новых записей напиши команду /add")

async def on_startup(bot):
  await bot.set_webhook(WEBHOOK_URL)

  result = await bot.get_webhook_info()

async def on_shutdown(bot):
  await bot.delete_webhook()

def main():
  dp = Dispatcher()
  dp.include_router(router)

  dp.startup.register(on_startup)

  bot = Bot(TG_BOT_TOKEN)

  app = web.Application()

  webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
  )

  webhook_requests_handler.register(app, path=WEBHOOK_PATH)

  setup_application(app, dp, bot=bot)
  web.run_app(app, host='0.0.0.0', port=int(os.getenv("APP_PORT", 8080)))

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  main()
