from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from src.keyaboards.keyboards import help_keyboard
from src.utils.handlers_helpers import send_help_info


router = Router()

@router.message(CommandStart())
async def handle_start_message(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Добро пожаловать в бота, \
                который скоро все будет знать! Напиши, что ты хочешь узнать? \
                Напишите запрос и бот напишет все, что знает.",
        reply_markup=help_keyboard
    )

@router.message(Command("menu"))
async def handle_open_keyboard(message: Message):
    await message.answer("Выберите опцию: ", reply_markup=help_keyboard)

@router.callback_query(F.data == "handle_help_button")
async def handle_help_button_callback(callback: CallbackQuery):
    await callback.answer()
    await send_help_info(callback.message)

@router.message(Command("help"))
async def handle_help_button(message: Message):
    await send_help_info(message)
