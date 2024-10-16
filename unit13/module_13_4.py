from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api: str = ''  # token to access the HTTP API
bot: Bot = Bot(token=api)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# выполнение функции только при получении сообщения /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    await message.answer('Привет! Я бот помогающий твоему здоровью')  # выводит сообщение в телеграмме

# выполнение функции только при получении сообщения 'Calories'
@dp.message_handler(text=['Calories'])
async def set_age(message: types.Message) -> None:
    await message.answer('Введите свой возраст.')  # выводит сообщение в телеграмме
    await UserState.age.set()

# выполнение функции при записи состояния
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

# выполнение функции только при получении любого другого сообщения
@dp.message_handler()
async def all_messages(message: types.Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
