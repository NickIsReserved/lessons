from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "BOT_TOKEN"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")
    # print("Введена команда /start.")

@dp.message_handler()
async def all_message(message):
    await message.answer(f"Введите команду /start, чтобы начать общение.")
    # print("Получено сообщение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)