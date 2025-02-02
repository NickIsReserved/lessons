from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions import get_all_products, is_included, add_user

api = "BOT_TOKEN"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    calc_age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

    def __init__(self):
        super().__init__()
        self.balance = 1000


# Создаем клавиатуру
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_calculate = KeyboardButton("Рассчитать")
    button_info = KeyboardButton("Информация")
    button_buy = KeyboardButton("Купить")
    button_register = KeyboardButton("Регистрация")
    keyboard.add(button_calculate, button_info, button_buy, button_register)
    return keyboard


# Создаем Inline-клавиатуру для продуктов
def get_buying_keyboard():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button_product1 = InlineKeyboardButton(text="Product1",
                                           callback_data="product_buying")
    button_product2 = InlineKeyboardButton(text="Product2",
                                           callback_data="product_buying")
    button_product3 = InlineKeyboardButton(text="Product3",
                                           callback_data="product_buying")
    button_product4 = InlineKeyboardButton(text="Product4",
                                           callback_data="product_buying")
    keyboard.add(button_product1, button_product2, button_product3,
                 button_product4)
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
async def set_calc_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:",
                              reply_markup=types.ReplyKeyboardRemove())
    await UserState.calc_age.set()
    await call.answer()


# Обработчик ввода возраста
@dp.message_handler(state=UserState.calc_age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(calc_age=message.text)
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

    calc_age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Упрощенная формула Миффлина - Сан Жеора для мужчин
    calories = (10 * weight) + (6.25 * growth) - (5 * calc_age) + 5

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


# Обработчик кнопки "Купить"
@dp.message_handler(lambda message: message.text == 'Купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()

    for i in range(len(products)):
        await message.answer(
            f"Название: Продукт {products[i][1]} | Описание: {products[i][2]} | Цена: {products[i][3]}")

        with open(f'{i + 1}.jpg', 'rb') as photo:
            await message.answer_photo(photo=photo)

    await message.answer("Выберите продукт для покупки:",
                         reply_markup=get_buying_keyboard())


# Обработчик Inline-кнопки 'product_buying'
@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Обработчик кнопки "Регистрация"
@dp.message_handler(lambda message: message.text == 'Регистрация')
async def sign_up(message: types.Message):
    """
    Начинаем процесс регистрации пользователя.
    """
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


# Обработчик ввода имени пользователя
@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    """
    Проверяем, существует ли пользователь с таким именем.
    Если нет, переходим к вводу email.
    """
    username = message.text

    # Проверяем, существует ли пользователь
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
        return  # Остаемся в состоянии RegistrationState.username

    await state.update_data(username=username)

    await message.answer("Введите свой email:")
    await RegistrationState.next()


# Обработчик ввода email
@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    """
    Сохраняем email и переходит к вводу возраста.
    """
    email = message.text

    await state.update_data(email=email)

    await message.answer("Введите свой возраст:")
    await RegistrationState.next()


# Обработчик ввода возраста
@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    """
    Сохраняем возраст, добавляем пользователя в базу данных и завершаем процесс регистрации.
    """
    age = message.text

    # Проверяем, что возраст является числом
    if not age.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте снова:")
        return

    await state.update_data(age=int(age))

    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = data['age']

    # Добавляем пользователя в базу данных
    add_user(username, email, age)

    await message.answer("Регистрация завершена! Спасибо за регистрацию.")
    await state.finish()


# Обработчик всех остальных сообщений
@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer(
        f"Пожалуйста, используйте кнопки для взаимодействия с ботом.",
        reply_markup=get_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
