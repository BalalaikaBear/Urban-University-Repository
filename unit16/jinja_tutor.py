from fastapi import FastAPI, Path, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory="unit16/templates_tutor")

# fastapi dev unit16/jinja_tutor.py - запуск файла

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
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages_db})

@app.get('/message/{message_id}')
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("message.html", {"request": request, "message": messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    if messages_db:
        message_id: int = max(messages_db, key=lambda m: m.id).id + 1
    else:
        message_id: int = 0
    messages_db.append(Message(id=message_id, text=message))
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages_db})

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

