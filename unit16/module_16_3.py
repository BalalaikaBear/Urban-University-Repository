from fastapi import FastAPI

app = FastAPI()

# fastapi dev unit16/module_16_3.py - запуск файла

users: dict = {'1': 'Имя: Example, возраст: 18'}

@app.get('/users')
async def get_users() -> dict:
    """Получение всех пользователей"""
    return users

@app.post('/user/{username}/{age}')
async def add_user(username: str, age: int) -> str:
    """Создание нового пользователя"""
    max_index = str(int(max(users, key=int)) + 1)
    users[max_index] = f"Имя: {username}, возраст: {age}"
    return f"User #{max_index} is registered"

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> str:
    """Переписывание информации о пользователе"""
    users[str(user_id)] = f"Имя: {username}, возраст: {age}"
    return f"User #{user_id} has been updated"

@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    """Удаление пользователя"""
    if str(user_id) in users:
        users.pop(str(user_id))
    return f"User #{user_id} was deleted"
