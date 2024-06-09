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
    print(f"Команда /start от: {message.from_user.first_name} - {message.from_user.username}({message.from_user.id})")
    web = WebAppInfo(url="https://bat-keen-robin.ngrok-free.app/")
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Тыкай", web_app=web))
    kb.adjust(1)
    await message.answer(
        text="Нихао, Мой Друг!\nВот тебе приложение, но только в телеграме :)",
        reply_markup=kb.as_markup()
    )
