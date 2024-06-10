import ast
import asyncio
import logging

from aiogram.types import FSInputFile
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types
from googletrans import Translator

import start_message
from functions.exercise import get_ex_dict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from db.db import create_connection, get_exercise_data

STATIC_FILES = "/static"
DB_FILE = Path(__file__).parent / "db/app_db.db"

# Словарь для хранения сессий доступа
admin_sessions = {}

app = FastAPI()
# Define the path to the templates directory
templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=templates_path)

# Mount the static files directory
app.mount(STATIC_FILES, StaticFiles(directory="static"), name="static")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return FileResponse('index.html')


@app.get("/exercise")
async def exercise(request: Request):
    print(f"\n\nПолучено с -> {request.url}")
    data = request.query_params.get("data")
    data = ast.literal_eval(data)
    print(type(data), ":", data)
    exercise: str = data.get("exercise", "No exercise")
    exercise: dict = get_ex_dict("static/json/exercises_co.json", exercise)
    print(20 * "=", "\n", exercise, "\n", 20 * "=")
    # user_id = data.get("userID", "No userID")

    ex_num = exercise['ex_name'].replace(" ", "_")
    print(ex_num)
    # Подключение к базе данных
    conn = create_connection(DB_FILE)

    with conn:
        rows = get_exercise_data(conn, exercise=ex_num)
    print(rows)

    # Подготовка данных для шаблона
    exercise_data = [{"first_name": row[0], "result": int(row[1])} for row in rows]

    ex_description = exercise['ex_description']
    if isinstance(ex_description, str):
        translator = Translator()
        ex_description = translator.translate(text=ex_description, dest="ru", src="en").text
        print(f"Переведено -> {ex_description}")
    else:
        ex_description = ""

    img_pth = f"/static/images/{exercise['ex_name']}.jpg"
    # Возврат другой HTML-страницы

    return templates.TemplateResponse("result.html", {"request": request,
                                                      "exercise": exercise['ex_name'],
                                                      "ex_rules": exercise['ex_rules'],
                                                      "ex_description": ex_description,
                                                      "ex_tags": exercise['ex_tags'],
                                                      "img_pth": img_pth,
                                                      "exercise_data": exercise_data
                                                      })


@app.post("/exercise")
async def send_web_message(request: Request):
    print(f"\n\nПолучено с -> {request.url}")
    data = await request.json()
    print(type(data), ":", data)


@app.get("/ranking")
async def get_ranking(request: Request):
    # Подключение к базе данных
    conn = create_connection(DB_FILE)

    with conn:
        cursor = conn.cursor()

        # Получение данных из таблицы Users
        cursor.execute("SELECT first_name, global_points FROM Users")
        users_data = cursor.fetchall()

    # Сортировка данных по глобальным очкам в убывающем порядке
    rows = sorted(users_data, key=lambda x: x[1], reverse=True)
    print(rows)

    # Подготовка данных для шаблона
    data = [{"first_name": row[0], "points": int(row[1])} for row in rows]

    # Добавление номера места
    for index, user in enumerate(data, start=1):
        user["rank"] = index

    return templates.TemplateResponse("ranking.html", {"request": request,
                                                       "ranking_data": data
                                                       })


@app.get("/admin")
async def admin_panel(request: Request):
    # token = request.query_params.get("token")
    # if not token or token not in admin_sessions:
    #     raise HTTPException(status_code=403, detail="Access forbidden")

    return templates.TemplateResponse("admin", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=80)
