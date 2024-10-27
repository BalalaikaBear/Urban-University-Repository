from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# машина состояний (Finite State Machine)
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# клавиатура в сообщении
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.callback_query import CallbackQuery

api: str = ''  # token to access the HTTP API
bot: Bot = Bot(token=api)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

# клавиатура
kb_buy: InlineKeyboardMarkup = InlineKeyboardMarkup(resize_keyboard=True)  # объект клавиатуры
# добавление кнопок в клавиатуру (n-элементов в строке)
kb_buy.add(InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
           InlineKeyboardButton(text='Формула расчёта', callback_data='formulas'))
kb_buy.add(InlineKeyboardButton(text='Купить', callback_data='buy'))

kb_products: InlineKeyboardMarkup = InlineKeyboardMarkup(resize_keyboard=True)
kb_products.add(InlineKeyboardButton(text='Product1', callback_data='product_buying'),
                InlineKeyboardButton(text='Product2', callback_data='product_buying'),
                InlineKeyboardButton(text='Product3', callback_data='product_buying'),
                InlineKeyboardButton(text='Product4', callback_data='product_buying'))


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# выполнение функции только при получении сообщения /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    await message.answer('Привет! Я бот помогающий твоему здоровью',  # выводит сообщение в телеграмме
                         reply_markup=kb_buy)  # вывод собственной клавиатуры

# РАСЧЕТ КАЛОРИЙ ---------------------------------------------------------------------------------------------------- *
# выполнение функций при срабатывании кнопки ---------------------------- /
@dp.callback_query_handler(text='formulas')  # <text> - ID кнопки
async def get_formulas(call: CallbackQuery):  # запрос обратного вызова от кнопки в сообщении
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()  # завершение срабатывания кнопки (разблокирует повторное нажатие кнопки)

@dp.callback_query_handler(text='calories')
async def set_age(call: CallbackQuery) -> None:
    await call.message.answer('Введите свой возраст.')  # выводит сообщение в телеграмме
    await call.answer()  # завершение срабатывания кнопки (разблокирует повторное нажатие кнопки)
    await UserState.age.set()

# выполнение функций при записи состояния ------------------------------- /
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message,  # сообщение, написанное пользователем
                     state: FSMContext) -> None:  # FSMContext - машина состояний (Finite State Machine)
    await state.update_data(age=float(message.text))  # запись значения в словарь под ключом 'age'
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message: types.Message,
                     state: FSMContext) -> None:
    await state.update_data(growth=float(message.text))  # запись значения в словарь под ключом 'growth'
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message,
                        state: FSMContext) -> None:
    await state.update_data(weight=float(message.text))  # запись значения в словарь под ключом 'weight'
    data: dict = await state.get_data()  # получение словаря
    await state.finish()  # необходимо закрыть "машину состояния", чтобы она сохранила свое состояние
    await message.answer(f'Ваша норма калорий ~ {10*data["weight"] + 6.25*data["growth"] - 5*data["age"] + 5}')

# ПОКУПКА ТОВАРОВ --------------------------------------------------------------------------------------------------- *
# выполнение функций при срабатывании кнопки ---------------------------- /
@dp.callback_query_handler(text='buy')  # <text> - ID кнопки
async def get_buying_list(call: CallbackQuery):  # запрос обратного вызова от кнопки в сообщении
    for i in range(1, 5):
        with open('files/1.jpg', 'rb') as img:
            await call.message.answer_photo(img, f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
    await call.message.answer('Выберите продукт для покупки', reply_markup=kb_products)
    await call.answer()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

# ------------------------------------------------------------------------------------------------------------------- *
# выполнение функции только при получении любого другого сообщения
@dp.message_handler()
async def all_messages(message: types.Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
