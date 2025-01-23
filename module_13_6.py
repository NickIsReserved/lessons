from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "BOT_TOKEN"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Создаем клавиатуру
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_calculate = KeyboardButton("Рассчитать")
    button_info = KeyboardButton("Информация")
    keyboard.add(button_calculate, button_info)
    return keyboard


# Создаем Inline-клавиатуру
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button_calories = InlineKeyboardButton(text="Рассчитать норму калорий",
                                           callback_data="calories")
    button_formulas = InlineKeyboardButton(text="Формулы расчёта",
                                           callback_data="formulas")
    keyboard.add(button_calories, button_formulas)
    return keyboard


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку 'Рассчитать', чтобы начать расчёт нормы калорий.",
        reply_markup=get_keyboard())


# Обработчик нажатия кнопки 'Рассчитать'
@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=get_inline_keyboard())


# Обработчик Inline-кнопки 'Формулы расчёта'
@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_text = (
        "Формула Миффлина-Сан Жеора для мужчин:\n"
        "Калории = (10 × вес в кг) + (6.25 × рост в см) - (5 × возраст в годах) + 5"
    )
    await call.message.answer(formula_text)
    await call.answer()


# Обработчик Inline-кнопки 'Рассчитать норму калорий'
@dp.callback_query_handler(lambda call: call.data == 'calories', state=None)
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:",
                              reply_markup=types.ReplyKeyboardRemove())
    await UserState.age.set()
    await call.answer()


# Обработчик ввода возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (в см):")
    await UserState.next()


# Обработчик ввода роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.next()


# Обработчик ввода веса и расчет калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Упрощенная формула Миффлина - Сан Жеора для мужчин
    calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал/день",
                         reply_markup=get_keyboard())
    await state.finish()


# Обработчик кнопки "Информация"
@dp.message_handler(lambda message: message.text == 'Информация')
async def send_info(message: types.Message):
    await message.answer(
        "Этот бот помогает рассчитать вашу норму калорий по формуле Миффлина - Сан Жеора. "
        "Нажмите 'Рассчитать', чтобы начать.",
        reply_markup=get_keyboard()
    )


# Обработчик всех остальных сообщений
@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer(
        f"Пожалуйста, используйте кнопки для взаимодействия с ботом.",
        reply_markup=get_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
