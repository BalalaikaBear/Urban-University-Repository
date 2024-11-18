from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# fastapi dev unit16/fastapi_tutor.py - запуск файла

messages_db = {"0": "First post in FastAPI"}

# виды запросов
# get - адрес в строке ?<переменная>=<значение>
# post - формы - оформить заказ в магазине
# put - запрос замены
# delete - запрос типа удаления

@app.get('/')  # при получении запроса типа '/' -> выполнить функцию
async def get_all_messages() -> dict:
    return messages_db

@app.get('/message/{message_id}')
async def get_message(message_id: str) -> dict:
    return messages_db[message_id]

@app.post('/message')
async def create_message(message: str) -> str:
    current_index = str(int(max(messages_db, key=int)) + 1)
    messages_db[current_index] = message
    return "Message created!"

@app.put('/message/{message_id}')
async def update_message(message_id: str, message: str) -> str:
    messages_db[message_id] = message
    return "Message updated!"

@app.delete('/message/{message_id}')
async def delete_message(message_id: str) -> str:
    messages_db.pop(message_id)
    return "Message deleted!"

@app.delete('/')
async def delete_all_messages() -> str:
    messages_db.clear()
    return "All messages were deleted!"

# при получении запроса типа '/id?username=<имя пользователя>&age=<возраст>' -> выполняется функция
# если было введено '/id' без уточняющего запроса -> вернет значения по умолчанию username=Bob и age=20
@app.get('/id')
async def id_paginator(username: str = "Bob", age: int = 20) -> dict:
    return {"User": username, "Age": age}

# Выполнение запроса типа '/user/<x>/<y>' --------------------------------------------------------------------------- *
@app.get('/user/A/B')
async def news() -> dict:
    return {"message": f" Hello, Tester!"}

# Path() - проверяет входимые элементы
# Annotated -
@app.get('/user/{username}/{id}')
async def news(username: Annotated[str, Path(min_length=3,
                                             max_length=15,
                                             description="Enter your username",
                                             example="Bob")],
               id: int = Path(ge=0,
                              le=100,
                              description="Enter your ID",
                              example=75)) -> dict:  # ge - >= 0, le - <= 100
    return {"message": f" Hello, {username} #{id}"}

# ------------------------------------------------------------------------------------------------------------------- *
