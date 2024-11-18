from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# fastapi dev unit16/fastapi_tutor.py - запуск файла

# виды запросов
# get - адрес в строке ?<переменная>=<значение>
# post - формы - оформить заказ в магазине
# put - запрос замены
# delete - запрос типа удаления

@app.get('/')  # при получении запроса типа '/' -> выполнить функцию
async def welcome() -> dict:
    return {"message": "Hello world"}

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
