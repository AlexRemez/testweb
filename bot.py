import ast
import asyncio
import logging

from aiogram.types import FSInputFile, CallbackQuery
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types
import start_message
from db import db
from functions.exercise import get_ex_dict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from functions.points import calc_points

from db.db import create_connection, get_exercise_data

API_TOKEN = ""
YOUR_CHAT_ID = "5691938305"  # Обновите после получения chat_id
STATIC_FILES = "/static"
DB_FILE = Path(__file__).parent / "db/app_db.db"

# app = FastAPI()
# # Define the path to the templates directory
# templates_path = Path(__file__).parent / "templates"
# templates = Jinja2Templates(directory=templates_path)
#
# # Mount the static files directory
# app.mount(STATIC_FILES, StaticFiles(directory="static"), name="static")
#
# # Настройка CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.callback_query()
async def handle(callback: CallbackQuery):
    data = callback.data
    data = data.split('!_!')
    ex_num = data[1].replace(' ', '_')
    exercise = get_ex_dict(json_file="static/json/exercises_co.json", ex_name=data[1])
    points = calc_points(exercise=exercise)
    user = dict(db.get_user(tg_id=data[0]))
    ex_points = user.get(ex_num)
    global_points = user['global_points']
    if global_points is None:
        global_points = points
        new_data = {ex_num: points, 'global_points': global_points}
        db.update_user(tg_id=data[0], data=new_data)
        await callback.message.edit_text(text="Готово", reply_markup=None)
    else:
        if ex_points is None:
            global_points += points
            new_data = {ex_num: points, 'global_points': global_points}
            db.update_user(tg_id=data[0], data=new_data)
            await callback.message.edit_text(text="Готово", reply_markup=None)
        else:
            await callback.message.edit_text(text="Уже есть результат!", reply_markup=None)





def add_routes(dispatcher: Dispatcher):
    dispatcher.include_router(start_message.start_router)


# @app.on_event("startup")
# async def on_startup():
#     asyncio.create_task(start_polling())
#
#
# @app.get("/")
# async def read_root():
#     return FileResponse('index.html')
#
#
# @app.get("/exercise")
# async def exercise(request: Request):
#     print(f"\n\nПолучено с -> {request.url}")
#     data = request.query_params.get("data")
#     data = ast.literal_eval(data)
#     print(type(data), ":", data)
#     exercise: str = data.get("exercise", "No exercise")
#     exercise: dict = get_ex_dict("static/json/exercises_co.json", exercise)
#     print(20 * "=", "\n", exercise, "\n", 20 * "=")
#     # user_id = data.get("userID", "No userID")
#
#     ex_num = exercise['ex_name'].replace(" ", "_")
#     print(ex_num)
#     # Подключение к базе данных
#     conn = create_connection(DB_FILE)
#
#     with conn:
#         rows = get_exercise_data(conn, exercise=ex_num)
#
#     # Подготовка данных для шаблона
#     exercise_data = [{"first_name": row[0], "result": int(row[1])} for row in rows]
#
#     img_pth = f"/static/images/{exercise['ex_name']}.jpg"
#     # Возврат другой HTML-страницы
#
#     return templates.TemplateResponse("result.html", {"request": request,
#                                                       "exercise": exercise['ex_name'],
#                                                       "ex_rules": exercise['ex_rules'],
#                                                       "ex_description": exercise['ex_description'],
#                                                       "ex_tags": exercise['ex_tags'],
#                                                       "img_pth": img_pth,
#                                                       "exercise_data": exercise_data
#                                                       })
#
#
# @app.post("/exercise")
# async def send_web_message(request: Request):
#     print(f"\n\nПолучено с -> {request.url}")
#     data = await request.json()
#     print(type(data), ":", data)
#
#
# @app.get("/ranking")
# async def get_ranking(request: Request):
#
#
#
#     return "SOON"


async def start_polling():
    logging.basicConfig(level=logging.INFO)
    add_routes(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_polling())
