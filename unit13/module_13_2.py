from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api: str = ''  # token to access the HTTP API
bot: Bot = Bot(token=api)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

# выполнение функции только при получении сообщения /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    print('Привет! Я бот помогающий твоему здоровью')

# выполнение функции только при получении любого другого сообщения
@dp.message_handler()
async def all_messages(message: types.Message) -> None:
    print("Введите команду '/start', чтобы начать общение")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
