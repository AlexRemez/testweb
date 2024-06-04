import asyncio
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types
import start_message

API_TOKEN = "6193754959:AAEGUA1cFmEQqP-8Rnm4SdXidiuJJ3YqQH4"
YOUR_CHAT_ID = "5691938305"  # Обновите после получения chat_id

app = FastAPI()

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
async def send_message(request: Request):
    data = await request.json()
    message = data.get("text", "No text provided")
    print(data)
    await bot.send_message(chat_id=YOUR_CHAT_ID, text=message)
    return {"status": "Message sent"}


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
    uvicorn.run(app, host='0.0.0.0', port=8000)
