import asyncio  # модуль асинхронного программирования

# определение корутины (coroutines) - (асинхронной) функции, выполнение которой можно приостановить и возобновить
async def start_strongman(name: str, power: int) -> None:
    print(f'Силач {name} начал соревнования.')
    for ball in range(1, 6):
        await asyncio.sleep(1/power)  # await останавливает дальнейшее выполнение кода, пока функция asyncio.sleep не выполнится
        print(f'Силач {name} поднял шар №{ball}.')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament() -> None:
    people = [('Pasha', 3),
              ('Denis', 4),
              ('Apollon', 5)]

    # asyncio.create_task запускает выполнение асинхронной функции
    # и продолжает последующее выполнение кода не дожидаясь выполнения функции
    tasks: list[asyncio.Task] = [asyncio.create_task(start_strongman(*people[0])),
                                 asyncio.create_task(start_strongman(*people[1])),
                                 asyncio.create_task(start_strongman(*people[2]))]

    for task in tasks:
        await task  # остановить дальнейшее выполнение кода, пока не выполнятся задачи

asyncio.run(start_tournament())  # запуск асинхронной функции, дальнейшее выполнение кода останавливается
