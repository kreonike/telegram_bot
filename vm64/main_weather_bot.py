import requests
import datetime
from config import weather_bot_token, open_weather_token
from aiogram import Bot, types

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(weather_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['wd'])
async def start_command(message: types.Message):
    await message.reply('../test')

@dp.message_handler()
async def get_weather(message: types.Message):

    city = 'Moscow'
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }


    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
          )
        data = r.json()
        #pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, я не пойму, что за погода.'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        await message.reply(f' Сегодня: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
              f' Погода в городе: {city}\n'
              f' Температура: {cur_weather}C° {wd}\n'
              f' Влажность: {humidity}\n'
              f' Давление: {pressure} мм.рт.ст\n'
              f' Ветер: {wind} м/с\n'
              f' Восход солнца: {sunrise_timestamp}\n'
              f' Закат солнца: {sunset_timestamp}\n'
              f' Продолжительность дня: {length_of_the_day}\n'
              f' Хорошего дня!'
        )



    except:
        await message.reply('Проверьте название города')

if __name__ == '__main__':
    executor.start_polling(dp)