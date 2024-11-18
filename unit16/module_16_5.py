from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="unit16/templates")

# fastapi dev unit16/module_16_5.py - запуск файла

# База данных
users: list = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/user/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.post('/user/{username}/{age}')
async def add_user(username: str, age: int) -> User:
    """Создание нового пользователя"""
    new_id: int = len(users)
    users.append(User(id=new_id, username=username, age=age))
    return users[new_id]

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    """Переписывание информации о пользователе"""
    try:
        users[user_id] = User(id=user_id, username=username, age=age)
        return users[user_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> User:
    """Удаление пользователя"""
    try:
        return users.pop(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
