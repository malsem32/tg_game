from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandObject
from fastapi_app.config import PUBLIC_URL
from aiogram.utils.deep_linking import create_start_link, decode_payload
from bot.pydantic_models.user_models import UserData
from bot.db.user_db import User_DB
from bot.db.slaves import Slaves_DB
from aiogram.types import UserProfilePhotos
from bot.create_bot import bot
from bot.config import TOKEN_BOT

start_router = Router()


@start_router.message(Command('start'))
async def start(message: types.Message, command: CommandObject):
    link = command.args
    user_info = User_DB().get_user_info_by_id(message.from_user.id)
    if user_info is None:
        if link and User_DB().check_user_for_invite_link(message.from_user.id) is None:
            photo_url = ''
            photos: UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
            if len(photos.photos) > 1:
                file = await bot.get_file(photos.photos[0][-1].file_id)
                photo_url = f'https://api.telegram.org/file/bot{TOKEN_BOT}/{file.file_path} '
            user_data = UserData(
                user_id=message.from_user.id,
                username=message.from_user.username if message.from_user.username else '',
                first_name=message.from_user.first_name if message.from_user.first_name else '',
                last_name=message.from_user.last_name if message.from_user.last_name else '',
                is_premium=False if message.from_user.is_premium is None else True,
                photo_url=photo_url
            )
            User_DB().check_user(user_data)
            User_DB().user_from_invite_link(user_data.user_id, link)
            user_id_invite = User_DB().get_user_from_invite_link(link) # пользователь который пригласил
            Slaves_DB().add_slave(user_id_invite, user_data.user_id)
            await message.answer(f"Вы зарегистрированы по реферальной ссылке")
            await bot.send_message(user_id_invite, f'Пользователь {message.from_user.first_name} | @{message.from_user.username} присоединился по вашей ссылке')
    else:
        await message.answer('Вы уже зарегистрированы в игре')
    webapp = types.WebAppInfo(url=PUBLIC_URL)
    but = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть приложение', web_app=webapp)]
    ])
    await message.answer('Нажмите кнопку', reply_markup=but)
