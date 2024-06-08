import asyncio
import logging

from aiogram.types import FSInputFile
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types
import start_message
from functions.exercise import get_ex_dict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
API_TOKEN = "6193754959:AAEGUA1cFmEQqP-8Rnm4SdXidiuJJ3YqQH4"
YOUR_CHAT_ID = "5691938305"  # Обновите после получения chat_id


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def add_routes(dispatcher: Dispatcher):
    dispatcher.include_router(start_message.start_router)


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_polling())


@app.post("/send-message")
async def send_web_message(request: Request):
    print(f"\n\nПолучено с -> {request.url}")
    data = await request.json()
    print(data)
    exercise: str = data.get("Exercise", "No exercise")
    exercise: dict = get_ex_dict("exercises_co.json", exercise)

    # user_id = data.get("userID", "No userID")
    # ФУНЦКИЯ ОТПРАВКИ УПРАЖНЕНИЯ В БОТА
    # text = f"<b>{exercise['ex_name']}</b>\n\n" \
    #        f"Description: {exercise['ex_description']}\n\n" \
    #        f"Rules: {exercise['ex_rules']}\n\n" \
    #        f"Tags: {exercise['ex_tags']}"
    # img_pth = FSInputFile(f"images/{exercise['ex_name']}.jpg")
    # await bot.send_photo(chat_id=user_id, photo=img_pth, caption=text, parse_mode="HTML")

    img_pth = f"images/{exercise['ex_name']}.jpg"
    # Возврат другой HTML-страницы
    return templates.TemplateResponse("result.html", {"request": request,
                                                      "exercise": exercise['ex_name'],
                                                      "ex_rules": exercise['ex_rules'],
                                                      "ex_description": exercise['ex_description'],
                                                      "ex_tags": exercise['ex_tags'],
                                                      "img_pth": img_pth

                                                      })






# @dp.message()
# async def echo(message: types.Message):
#     await message.answer(message.text)


async def start_polling():
    logging.basicConfig(level=logging.INFO)
    add_routes(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)
