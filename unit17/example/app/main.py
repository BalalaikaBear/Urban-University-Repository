from fastapi import FastAPI
from routers import category

app = FastAPI()

# fastapi dev unit17/example/app/main.py - запуск файла

@app.get("/")
async def welcome():
    return {"message": "My shop"}

# позволяет подключать дополнительные внешние роуты, и легко масштабировать приложение
app.include_router(category.router)