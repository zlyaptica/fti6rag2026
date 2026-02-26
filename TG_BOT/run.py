import os
import sys
import logging
import asyncio 
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
llm_path = os.path.join(os.path.dirname(current_dir), 'LLM')
if llm_path not in sys.path:
    sys.path.insert(0, llm_path)
    print(f"Добавлен путь к LLM: {llm_path}")

try:
    from run import QwenLLM, get_llm_instance
    MODEL_FOLDER_PATH = os.path.join(llm_path, 'Qwen3-0.6B')
    print(f"Путь к папке с моделью: {MODEL_FOLDER_PATH}")
except ImportError as e:
    print(f"Ошибка импорта модели: {e}")
    raise

load_dotenv(".env")
tg_token = os.getenv("TG_BOT_APIKEY")
if not tg_token:
    raise ValueError("Токен телеграм бота не найден")

dp = Dispatcher(storage=MemoryStorage())
llm_model = None

def create_llm_model():
    global MODEL_FOLDER_PATH
    return QwenLLM(model_path=MODEL_FOLDER_PATH)

@dp.message(CommandStart())
async def handle_start_message(message: Message):
    global llm_model
    await message.answer(
        f"Привет, {message.from_user.full_name}! Добро пожаловать в бота с искусственным интеллектом!"
    )

    if llm_model is None:
        loading_msg = await message.answer("Загружаю модель искусственного интеллекта. Это может занять несколько секунд...")
        
        try:
            llm_model = create_llm_model()
            await loading_msg.edit_text("Модель успешно загружена! Теперь вы можете задавать вопросы.")
        except Exception as e:
            await loading_msg.edit_text(f"Ошибка загрузки модели: {str(e)[:100]}...")
            logging.error(f"Ошибка загрузки модели: {e}")

@dp.message(F.text)
async def handle_question(message: Message):
    global llm_model
    if llm_model is None:
        await message.answer("Модель еще не загружена. Пожалуйста, напишите /start")
        return
    
    try:
        thinking_msg = await message.answer("Думаю над ответом...")
        response = llm_model.ask(message.text)
        await thinking_msg.delete()
        if len(response) > 4096:
            for i in range(0, len(response), 4096):
                await message.answer(response[i:i+4096])
        else:
            await message.answer(response)
            
    except Exception as e:
        logging.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("Извините, произошла ошибка при обработке запроса. Попробуйте позже.")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    bot = Bot(token=tg_token)
    logging.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())