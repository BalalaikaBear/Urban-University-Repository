from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# fastapi dev unit16/module_16_2.py - запуск файла

@app.get('/')  # при получении запроса типа '/' -> выполнить функцию
async def main() -> str:
    return 'Главная страница'

@app.get('/user/admin')  # при получении запроса типа '/user/admin' -> выполнить функцию
async def admin() -> str:
    return 'Вы вошли как администратор'

@app.get('/user/{user_id}')  # при получении запроса типа '/user/<текст>' -> выполнить функцию
async def user_id_func(user_id: Annotated[int, Path(ge=1, le=100,
                                                    description="Enter User ID",
                                                    example="1")]) -> str:
    return f'Вы вошли как пользователь №{user_id}'

@app.get('/user/{username}/{age}')  # при получении запроса типа '/user/<Имя пользователя>/<Возраст>' -> выполнить функцию
async def user(username: Annotated[str, Path(min_length=5, max_length=20,
                                             description="Enter username",
                                             example="Leonardo")],
               age: Annotated[int, Path(ge=18, le=120,
                                        description="Enter age",
                                        example=45)]) -> str:
    return f'Информация о пользователе: Имя: {username}, Возраст {age}'
