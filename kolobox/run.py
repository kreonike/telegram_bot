import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import token
from config import kinopoisk

import keyboards as kb
from aiogram import F

bot = Bot(token=token)
dp = Dispatcher()


def komedy():
    url = "https://api.kinopoisk.dev/v1.4/movie?rating.imdb=8-10&year=2023&year=2024&genres.name=комедия"
    #headers = {"accept": "application/json"}
    headers = {"X-API-KEY": kinopoisk}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def drama():
    url = "https://api.kinopoisk.dev/v1.4/movie?rating.imdb=8-10&year=2023&year=2024&genres.name=драма"
    #headers = {"accept": "application/json"}
    headers = {"X-API-KEY": kinopoisk}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def fantastik():
    url = "https://api.kinopoisk.dev/v1.4/movie?rating.imdb=8-10&year=2023&year=2024&genres.name=фантастика"
    #headers = {"accept": "application/json"}
    headers = {"X-API-KEY": kinopoisk}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('Привет, фильмы какого жанда Вас интересуют ?', reply_markup=kb.main)





@dp.message(F.text == "Комедия")
async def with_puree(message: Message):
    await message.reply('Отличный выбор')
    data = komedy()
    k_data = []
    string = ''
    for i in data['docs']:
        name = i['name']
        alternativeName = i['alternativeName']
        description = i['description']
        type = i['type']
        year = i['year']
        rating = i['rating']['imdb']
        genres = i['genres']

        k_data.append('Название Фильма: ')
        k_data.append(name)
        k_data.append('\n')
        k_data.append('Оригинальное название: ')
        k_data.append(alternativeName)
        k_data.append('\n')
        k_data.append('Описание: ')
        k_data.append(description)
        k_data.append('\n')
        k_data.append('Тип: ')
        k_data.append(type)
        k_data.append('\n')
        k_data.append('Год выпуска: ')
        k_data.append(year)
        k_data.append('\n')
        k_data.append('Рейтинг: ')
        k_data.append(rating)
        k_data.append('\n')
        k_data.append('Жанр: ')
        k_data.append(genres)
        k_data.append('\n')
        k_data.append('\n')

    for t in k_data:
        string += str(t)

    print(string)
    await message.reply(string)

    # print(f' Название фильма:', name, '\n'
        #       f' Оригинальное название:,', alternativeName, '\n'
        #       f' Описание:,', description, '\n')



    # print(k_data)
    # print(string)
    # await message.reply(string)
        # print(f' Название фильма:', name, "\n"
        #                                   f' Оригинальное название:', alternativeName, "\n"
        #                                                                                f' Год:', year, "\n"
        #                                                                                                f' Описание:',
        #       description, "\n"
        #                    f' Тип:', type, "\n"
        #                                    f' Рейтинг:', rating, "\n"
        #                                                          f' Жанр:', genres), "\n"
        # print("\n")


@dp.message(F.text == "Драма")
async def without_puree(message: Message):
    await message.reply('Отличный выбор')
    data = drama()
    k_data = []
    string = ''
    for i in data['docs']:
        name = i['name']
        alternativeName = i['alternativeName']
        description = i['description']
        type = i['type']
        year = i['year']
        rating = i['rating']['imdb']
        genres = i['genres']

        k_data.append('Название Фильма: ')
        k_data.append(name)
        k_data.append('\n')
        k_data.append('Оригинальное название: ')
        k_data.append(alternativeName)
        k_data.append('\n')
        k_data.append('Описание: ')
        k_data.append(description)
        k_data.append('\n')
        k_data.append('Тип: ')
        k_data.append(type)
        k_data.append('\n')
        k_data.append('Год выпуска: ')
        k_data.append(year)
        k_data.append('\n')
        k_data.append('Рейтинг: ')
        k_data.append(rating)
        k_data.append('\n')
        k_data.append('Жанр: ')
        k_data.append(genres)
        k_data.append('\n')
        k_data.append('\n')

    for t in k_data:
        string += str(t)

    print(string)
    await message.reply(string)
    # for i in data['docs']:
    #     name = i['name']
    #     alternativeName = i['alternativeName']
    #     description = i['description']
    #     type = i['type']
    #     year = i['year']
    #     rating = i['rating']['imdb']
    #     genres = i['genres']
    #     print(f' Название фильма:', name, "\n"
    #                                       f' Оригинальное название:', alternativeName, "\n"
    #                                                                                    f' Год:', year, "\n"
    #                                                                                                    f' Описание:',
    #           description, "\n"
    #                        f' Тип:', type, "\n"
    #                                        f' Рейтинг:', rating, "\n"
    #                                                              f' Жанр:', genres), "\n"
    #     print("\n")


@dp.message(F.text == "Фантастика")
async def without_puree(message: Message):
    await message.reply('Отличный выбор')
    data = fantastik()
    k_data = []
    string = ''
    for i in data['docs']:
        name = i['name']
        alternativeName = i['alternativeName']
        description = i['description']
        type = i['type']
        year = i['year']
        rating = i['rating']['imdb']
        genres = i['genres']

        k_data.append('Название Фильма: ')
        k_data.append(name)
        k_data.append('\n')
        k_data.append('Оригинальное название: ')
        k_data.append(alternativeName)
        k_data.append('\n')
        k_data.append('Описание: ')
        k_data.append(description)
        k_data.append('\n')
        k_data.append('Тип: ')
        k_data.append(type)
        k_data.append('\n')
        k_data.append('Год выпуска: ')
        k_data.append(year)
        k_data.append('\n')
        k_data.append('Рейтинг: ')
        k_data.append(rating)
        k_data.append('\n')
        k_data.append('Жанр: ')
        k_data.append(genres)
        k_data.append('\n')
        k_data.append('\n')

    for t in k_data:
        string += str(t)

    print(string)
    await message.reply(string)

def data_result(data):
    return



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    asyncio.run(main())

