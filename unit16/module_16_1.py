from fastapi import FastAPI

app = FastAPI()

# fastapi dev unit16/module_16_1.py - запуск файла

@app.get('/')  # при получении запроса типа '/' -> выполнить функцию
async def main() -> str:
    return 'Главная страница'

@app.get('/user/admin')  # при получении запроса типа '/user/admin' -> выполнить функцию
async def admin() -> str:
    return 'Вы вошли как администратор'

@app.get('/user/{user_id}')  # при получении запроса типа '/user/<текст>' -> выполнить функцию
async def user_id_func(user_id: str) -> str:
    return f'Вы вошли как пользователь №{user_id}'

@app.get('/user')  # при получении запроса типа '/user?username=<Имя пользователя>&age=<Возраст>' -> выполнить функцию
async def user(username: str, age: str) -> str:
    return f'Информация о пользователе: Имя: {username}, Возраст {age}'
