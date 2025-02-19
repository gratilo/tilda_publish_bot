import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from tilda_api import TildaApi
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TG_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

tilda = TildaApi(config.TILDA_PUBLIC_KEY, config.TILDA_SECRET_KEY)

class PublishPost(StatesGroup):
    title = State()
    description = State()
    text = State()
    images = State()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Привет! Я бот для публикации постов на Tilda. Отправь мне заголовок, описание и текст поста.")
    await PublishPost.title.set()


@dp.message_handler(state=PublishPost.title)
async def get_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Отлично! Теперь отправь мне описание поста.")
    await PublishPost.next()


@dp.message_handler(state=PublishPost.description)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Отлично! Теперь отправь мне текст поста.")
    await PublishPost.next()


@dp.message_handler(state=PublishPost.text)
async def get_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Отлично! Теперь отправь мне 1-3 изображения для поста.")
    await PublishPost.next()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=PublishPost.images)
async def get_images(message: types.Message, state: FSMContext):
    data = await state.get_data()

    #Скачивание фото
    images = []
    for photo in message.photo:
        file = await bot.get_file(photo.file_id)
        file_path = file.file_path
        images.append(f"https://api.telegram.org/file/bot{config.TG_BOT_TOKEN}/{file_path}")

    #Публикация
    page_id = tilda.create_post(title=data["title"], description=data["description"], text=data["text"], images=images)

    if page_id:
        await message.answer("Пост успешно опубликован!")
    else:
        await message.answer("Произошла ошибка при публикации поста.")

    await state.finish()



if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)