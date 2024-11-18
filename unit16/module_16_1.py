from fastapi import FastAPI

app = FastAPI()

# fastapi dev unit16/module_16_1.py - запуск файла

@app.get('/')
async def main() -> str:
    return 'Главная страница'

@app.get('/user/admin')
async def admin() -> str:
    return 'Вы вошли как администратор'

@app.get('/user/{user_id}')
async def user_id_func(user_id: str) -> str:
    return f'Вы вошли как пользователь №{user_id}'

@app.get('/user')
async def user(username: str, age: str) -> str:
    return f'Информация о пользователе: Имя: {username}, Возраст {age}'
