from fastapi import FastAPI
from routers import task, user

app = FastAPI()

# fastapi dev unit17/app/main.py - запуск файла

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

# позволяет подключать дополнительные внешние роуты, и легко масштабировать приложение
app.include_router(task.router)
app.include_router(user.router)