from aiogram import Router, types, F
from aiogram.filters import Command

from aiohttp.web_request import Request
from aiogram.types import FSInputFile, CallbackQuery, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_router = Router()


@start_router.message(Command('start'))
async def start_command_handler(message: types.Message):
    """
    Обработчик команды /start
    """

    web = WebAppInfo(url="https://alexremez.github.io/test_web_2/")
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Тыкай", web_app=web))
    kb.adjust(1)
    await message.answer(
        text="Нихао, Мой Друг!\nВот тебе приложение, но только в телеграме :)",
        reply_markup=kb.as_markup()
    )


