from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = "BOT_TOKEN"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer(
        "Привет! Напиши 'Calories', чтобы начать расчет нормы калорий.")


# Обработчик текстового сообщения 'Calories'
@dp.message_handler(lambda message: message.text == 'Calories')
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


# Обработчик ввода возраста
@dp.message_handler(state = UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост (в см):")
    await UserState.next()


# Обработчик ввода роста
@dp.message_handler(state = UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес:")
    await UserState.next()


# Обработчик ввода веса и расчет калорий
@dp.message_handler(state = UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Упрощенная формула Миффлина - Сан Жеора для мужчин
    calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал/день")
    await state.finish()


@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer(f"Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
