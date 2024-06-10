from aiogram import Router, types, F, Bot
from aiogram.filters import Command

from aiohttp.web_request import Request
from aiogram.types import FSInputFile, CallbackQuery, WebAppInfo, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from db import db

start_router = Router()


@start_router.message(Command('start'))
async def start_command_handler(message: types.Message, bot: Bot):
    """
    Обработчик команды /start
    """
    print(f"Команда /start от: {message.from_user.first_name} - {message.from_user.username}({message.from_user.id})")
    if db.get_user(message.from_user.id) is None:
        db.add_user(tg_id=message.from_user.id,
                    first_name=message.from_user.first_name,
                    username=message.from_user.username)
    #     user_profile_photo: types.UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
    #     if len(user_profile_photo.photos[0]) > 0:
    #         file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
    #         await bot.download_file(file.file_path, f'static/profile_photos/{message.from_user.id}.png')
    #     else:
    #         print('У пользователя нет фото в профиле.')



    web = WebAppInfo(url="https://bat-keen-robin.ngrok-free.app/")
    admin_web = WebAppInfo(url="https://bat-keen-robin.ngrok-free.app/admin")
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Открыть", web_app=web))
    if message.from_user.id == 5691938305 or message.from_user.id == 131956265:
        kb.add(InlineKeyboardButton(text="Админка", web_app=admin_web))
    kb.adjust(1)
    await message.answer(
        text="Приложение откроет доступ к множеству упражнений для развития технической и тактической составляющей игры в бильярд.\n\nЧтобы начать пользоваться приложением нажмите кнопку 'Открыть' ниже.\n",
        reply_markup=kb.as_markup()
    )
