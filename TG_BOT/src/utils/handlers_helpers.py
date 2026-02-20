from aiogram.types import Message


async def send_help_info(message: Message):
    await message.answer("Я могу найти любую информацию")
