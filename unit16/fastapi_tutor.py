from fastapi import FastAPI, Path, Body, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()

# fastapi dev unit16/fastapi_tutor.py - запуск файла

# База данных
messages_db: list = []

class Message(BaseModel):
    id: int = None
    text: str

# виды запросов
# get - адрес в строке ?<переменная>=<значение>
# post - формы - оформить заказ в магазине
# put - запрос замены
# delete - запрос типа удаления

@app.get('/')  # при получении запроса типа '/' -> выполнить функцию
async def get_all_messages() -> List[Message]:
    return messages_db

@app.get('/message/{message_id}')
async def get_message(message_id: int) -> Message:
    try:
        return messages_db[message_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.post('/message')
async def create_message(message: Message) -> str:
    message_id: int = len(messages_db)
    messages_db.append(message)
    return "Message created!"

@app.put('/message/{message_id}')
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message: Message = messages_db[message_id]
        edit_message.text = message
        return "Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.delete('/message/{message_id}')
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} was deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

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
