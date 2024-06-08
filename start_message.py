from aiogram import Router, types, F, Bot
from aiogram.filters import Command

from aiohttp.web_request import Request
from aiogram.types import FSInputFile, CallbackQuery, WebAppInfo, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


start_router = Router()


@start_router.message(Command('start'))
async def start_command_handler(message: types.Message):
    """
    Обработчик команды /start
    """

    web = WebAppInfo(url="https://alexremez.github.io/test_web_2/")
    web2 = WebAppInfo(url="https://alexremez.github.io/testweb/")
    kb2 = ReplyKeyboardBuilder()
    kb2.add(KeyboardButton(text="⭐️WEB", web_app=web2))
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Тыкай", web_app=web2))
    kb.adjust(1)
    await message.answer(
        text="Нихао, Мой Друг!\nВот тебе приложение, но только в телеграме :)",
        reply_markup=kb.as_markup()
    )


@start_router.message(types.Message)
async def get_data(web_app_data: types.WebAppData):
    print("OKKKKKKKKKKKKKKKKKKK")
    print(web_app_data)
    data = web_app_data.json()
    print(data)


