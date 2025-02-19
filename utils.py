from aiogram import types
from bot import bot
import config

async def download_images(message: types.Message):
    """Скачивает фото из сообщения и возвращает URL"""
    images = []
    for photo in message.photo[-1:]:  # Берем лучшее качество
        file = await bot.get_file(photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{config.TG_BOT_TOKEN}/{file.file_path}"
        images.append(file_url)
    return images
