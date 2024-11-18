from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# fastapi dev unit16/module_16_4.py - запуск файла

# База данных
users: list = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/users')
async def get_users() -> list[User]:
    """Получение всех пользователей"""
    return users

@app.post('/user/{username}/{age}')
async def add_user(username: str, age: int) -> User:
    """Создание нового пользователя"""
    new_id: int = len(users) + 1
    users.append(User(id=new_id, username=username, age=age))
    return users[new_id-1]

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    """Переписывание информации о пользователе"""
    try:
        users[user_id-1] = User(id=user_id, username=username, age=age)
        return users[user_id-1]
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> User:
    """Удаление пользователя"""
    try:
        return users.pop(user_id-1)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
