# -*- encoding: utf-8 -*-
import logging
import nmslib
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.markdown import link
from utils.htmlprocessing import get_name_for_url, get_url_of_face_with_id
from utils.findface import get_face_descriptor

AIOGRAM_API_TOKEN = os.getenv('AIOGRAM_API_TOKEN')

logging.basicConfig(level=logging.INFO)
# Настройки nmslib
index = nmslib.init(method='hnsw', space='l2',
                        data_type=nmslib.DataType.DENSE_VECTOR)
index.loadIndex('embeddings.bin')
query_time_params = {'efSearch': 400}
index.setQueryTimeParams(query_time_params)
# Настройки aiogram
bot = Bot(token = AIOGRAM_API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm FindCloneBot!\n" +
                "Help you find people's by photo.\n" +
                "Just send me photo and i'll try to find.")

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply("I can't undersand you!\n" +
        "If you need help, send me /help \n" +
        "Or just send me photo!")

@dp.message_handler(content_types = ['photo'])
async def photo_message(message: types.Message):
    photo_path = 'photos/' + str(message.message_id) + '.jpg'
    await message.photo[-1].download(photo_path)
    await message.reply('Wait a sec...')
    embedding = get_face_descriptor(photo_path)
    if embedding is None:
        await bot.delete_message(message.chat.id, message.message_id + 1)
        await message.reply("I can't find a face in this photo, try to send another")
        # Перемещаем фотографии без лица в отдельную папку
        os.rename(photo_path, f'photos/withoutface/{message.message_id}.jpg')
        return
    ids, _ = index.knnQuery(embedding, k=3)
    urls = [get_url_of_face_with_id(ids[0]), get_url_of_face_with_id(ids[1]), get_url_of_face_with_id(ids[2])]
    url_names = []
    for url in urls:
        url_names.append(get_name_for_url(url))
    await bot.delete_message(message.chat.id, message.message_id + 1)
    await message.reply('Most similar people\'s:\n\n'+ link(url_names[0],urls[0]) + '\n\n' \
                        + link(url_names[1],urls[1]) + '\n\n' + link(url_names[2],urls[2]), \
                        parse_mode = ParseMode.MARKDOWN)
    await message.reply('If you wanna try again, just send me a photo')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)