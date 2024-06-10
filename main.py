import ast
import math

from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator

from functions.exercise import get_ex_dict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from db import db

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
    exercise: str = data.get("exercise", "No exercise")
    exercise: dict = get_ex_dict("static/json/exercises_co.json", exercise)

    ex_num = exercise['ex_name'].replace(" ", "_")
    # Подключение к базе данных
    conn = db.create_connection(DB_FILE)

    with conn:
        rows = db.get_exercise_data(conn, exercise=ex_num)

    # Подготовка данных для шаблона
    exercise_data = [{"first_name": row[0], "result": math.ceil(float(row[1]))} for row in rows]

    ex_description = exercise['ex_description']
    # if isinstance(ex_description, str):
    #     translator = Translator()
    #     ex_description = translator.translate(text=ex_description, dest="ru", src="en").text
    # else:
    #     ex_description = ""

    img_pth = f"/static/images/{exercise['ex_name']}.jpg"
    # Возврат другой HTML-страницы

    tg_id = data.get("tg_id", "No tg_id")
    user = db.get_user(tg_id=tg_id)
    user_result = user[ex_num]
    if user_result == 0 or user_result is None:
        send_res = True
    else:
        send_res = False

    return templates.TemplateResponse("result.html", {"request": request,
                                                      "exercise": exercise['ex_name'],
                                                      "ex_rules": exercise['ex_rules'],
                                                      "ex_description": ex_description,
                                                      "ex_tags": exercise['ex_tags'],
                                                      "img_pth": img_pth,
                                                      "exercise_data": exercise_data,
                                                      "send_res": send_res
                                                      })


@app.get("/ranking")
async def get_ranking(request: Request):
    # Подключение к базе данных
    conn = db.create_connection(DB_FILE)

    with conn:
        cursor = conn.cursor()

        # Получение данных из таблицы Users
        cursor.execute("SELECT first_name, global_points FROM Users WHERE global_points IS NOT NULL ")
        users_data = cursor.fetchall()

    # Сортировка данных по глобальным очкам в убывающем порядке
    rows = sorted(users_data, key=lambda x: x[1], reverse=True)

    # Подготовка данных для шаблона
    data = [{"first_name": row[0], "points": row[1]} for row in rows]

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

    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/admin/users")
async def read_users(request: Request, query: str = "", message: str = None):
    conn = db.create_connection(DB_FILE)

    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tg_id, first_name FROM Users WHERE first_name LIKE ?", ('%' + query + '%',))
        users = cursor.fetchall()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users, "message": message})


@app.get("/admin/user/{user_id}")
async def read_user(request: Request, user_id: int):
    user: dict = db.get_user(user_id)
    print(user)
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})


@app.post("/update_user_data")
async def update_user_data(request: Request):
    data = await request.json()

    db.update_user(tg_id=int(data["tg_id"]),
                   first_name=str(data["first_name"]),
                   username=str(data["username"]),
                   global_points=data["global_points"])


@app.get("/admin/users/create_user")
async def create_user(request: Request):
    return templates.TemplateResponse("a_user_create_user.html", {"request": request})


@app.post("/admin/delete_user")
async def delete_user(request: Request):
    data = await request.json()
    db.delete_user(tg_id=int(data["tg_id"]))
    return {"success": True}


@app.post("/admin/users/create_user")
async def create_user(request: Request):
    data = await request.json()
    db.add_user(
        tg_id=int(data["tg_id"]),
        first_name=str(data["first_name"]),
        username=str(data["username"])
    )
    return {"success": True, "user_id": data["tg_id"]}


@app.post("/submit_result")
async def submit_result(request: Request):
    data = await request.json()
    from bot import bot
    text = f"Заявка от пользователя: {data['tg_id']}\n" \
           f"Упражнение: {data['exercise']}"

    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Подтвердить", callback_data=f"{data['tg_id']}!_!{data['exercise']}"))

    await bot.send_message(chat_id=5691938305, text=text, reply_markup=kb.as_markup())


@app.post("/send_result")
async def send_result(request: Request, verification: str = Form(...), attempt: str = Form(...)):
    from bot import bot
    if verification == "verified":
        if attempt == "single":
            text = f"Ваша заявка принята:" \
                   f"\n\nПришлите видео выполенного упражнения." \
                   f"\nПосле проверки ваш результат появится в рейтинге."
        elif attempt == "ten_attempts":
            text = f"Ваша заявка принята:" \
                   f"\n\nПришлите видео с 10-ю попытками." \
                   f"\nПосле проверки ваш результат появится в рейтинге и будет учитываться в рейтинге." \
                   f"Вы сможете улучшить результат в дальнейшем."
    elif attempt == "not_verified":
        text = f"Ваша заявка принята:" \
               f"\n\n Ваш результат будет добавлен в рейтинг без верификации и не будет учитываться в конкурсе." \
               f"Вы сможете улучшить результат в дальнейшем."

    # await bot.sendMessage()

    return RedirectResponse(url="/", status_code=303)
    # from bot import bot
    # text = f"Заявка от пользователя: {data['tg_id']}\n" \
    #        f"Упражнение: {data['exercise']}"
    #
    # kb = InlineKeyboardBuilder()
    # kb.add(InlineKeyboardButton(text="Подтвердить", callback_data=f"{data['tg_id']}!_!{data['exercise']}"))
    #
    # await bot.send_message(chat_id=5691938305, text=text, reply_markup=kb.as_markup())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=80)
