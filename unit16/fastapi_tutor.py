from fastapi import FastAPI

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
async def news(first_name: str, last_name: str) -> dict:
    return {"message": f" Hello, Tester!"}

@app.get('/user/{first_name}/{last_name}')
async def news(first_name: str, last_name: str) -> dict:
    return {"message": f" Hello, {first_name} {last_name}"}

# ------------------------------------------------------------------------------------------------------------------- *
