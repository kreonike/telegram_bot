import telebot
import requests
import os
from ping3 import ping
import pyowm
from pyowm import OWM
import glob, random
from glob import glob
import datetime
#from deepface import DeepFace
import json

# from aiogram import Bot, types
#
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor

while True:
    try:
        print('test')
        version ='bot version 0.58 alfa'

        bot = telebot.TeleBot("1342082221:AAGozdQD2pzPta-VEB9WFZlHelYEMPHo2lA")

        open_weather_token = '8d5998d11364d68d5c80b17c7eb15c05'
        #open_weather_token =  '8b0359d111213069f947d8075b3d6a1e'

        @bot.message_handler(commands=['help'])
        def send_uptime(message):
            # help = f'для помощи наберите /help'
            mess = 'поликлиника 1: /pol1,\n' \
                   'поликлиника 2: /pol2,\n' \
                   'поликлиника 3: /pol3,\n' \
                   'поликлиника 4: /pol4,\n' \
                   'статус: /status, \n' \
                   'погода: /weather, \n' \
                   'какой сегодня праздник: /holidays, \n' \
                   'анализатор ёбел: /eblo \n'

            bot.send_message(message.chat.id, mess)
            bot.send_message(message.chat.id, version)




        @bot.message_handler(commands=['pol1'])
        def send_uptime_pol1(message):
            result = requests.post(
                'https://api.uptimerobot.com/v2/getMonitors?api_key=ur110801-80feb7f4039798496a1928ab&format=json')
            data = result.json()
            monitors = data['monitors']
            print(data)

            # print(data.values())
            for val in monitors:
                status = val['status']
                frendlyName = val['friendly_name']
                monitorUrl = val['url']
                if status == 2:
                    status = 'UP'
                elif status == 8 or status == 9:
                    status = 'DOWN'

                print(f' {frendlyName}, {monitorUrl}, {status}')


                if frendlyName == 'work':
                    frendlyName = 'pol1'
                    bot.send_message(message.chat.id, f' {frendlyName}, {monitorUrl}, {status}')


        @bot.message_handler(commands=['pol3'])
        def send_uptime_pol3(message):
            global frendlyName
            result = requests.post(
                'https://api.uptimerobot.com/v2/getMonitors?api_key=ur110801-80feb7f4039798496a1928ab&format=json')
            data = result.json()
            monitors = data['monitors']

            for val in monitors:
                status = val['status']
                frendlyName = val['friendly_name']
                monitorUrl = val['url']
                if status == 2:
                    status = 'UP'
                elif status == 8 or status == 9:
                    status = 'DOWN'

                print(f' test {frendlyName}, {monitorUrl}, {status}')

                if frendlyName == 'pol3':
                    frendlyName = 'pol3'
                    bot.send_message(message.chat.id, f' {frendlyName}, {monitorUrl}, {status}')


        @bot.message_handler(commands=['status'])
        def send_uptime_pol1(message):
            result = requests.post(
                'https://api.uptimerobot.com/v2/getMonitors?api_key=ur110801-80feb7f4039798496a1928ab&format=json')
            data = result.json()
            monitors = data['monitors']
            print(data)

            for val in monitors:
                status = val['status']
                frendlyName = val['friendly_name']
                monitorUrl = val['url']
                if status == 2:
                    status = 'UP'
                elif status == 8 or status == 9:
                    status = 'DOWN'

                print(f' {frendlyName}, {monitorUrl}, {status}')

                if frendlyName == 'work':
                    frendlyName = 'pol1'
                    bot.send_message(message.chat.id, f' {frendlyName}, {monitorUrl}, {status}')
                elif frendlyName == 'pol3':
                    frendlyName = 'pol3'
                    bot.send_message(message.chat.id, f' {frendlyName}, {monitorUrl}, {status}')

            def ecp(ecp):
                resp = ping(ecp)

                if resp == False:
                    bot.send_message(message.chat.id, f' ecp.mznn.ru -->> Network Error')
                else:
                    bot.send_message(message.chat.id, f'ecp.mznn.ru -->> Network Active ')

            ecp('ecp.mznn.ru')




        @bot.message_handler(commands=['weather'])
        def weather2(message):

            city = 'Nizhniy Novgorod'
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
                print(data)

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

                bot.send_message(message.chat.id,
                      f' Сегодня: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
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
                print('какая-то ошибка')

        #############################################







        @bot.message_handler(commands=['porn'])
        def start(message):
            photo = open('porn/' + random.choice(os.listdir('porn')), 'rb')
            bot.send_photo(message.chat.id, photo)


        @bot.message_handler(commands=['trans'])
        def start(message):
            photo = open('trans/' + random.choice(os.listdir('trans')), 'rb')
            bot.send_photo(message.chat.id, photo)



        ##################
        #PARSER
        ################
        import requests
        from bs4 import BeautifulSoup

        @bot.message_handler(commands=['holidays'])
        def holidays(message):
            print('test_holidays')



            # bot.send_message(message.chat.id, f' Праздники на сегодня: {datetime.datetime.now().strftime("%Y-%m-%d")}\n'
            #                                   f'пансинг с сайта: https://my-calend.ru/holidays\n')




            link = "https://my-calend.ru/holidays"
            responce = requests.get(link).text
            soup = BeautifulSoup(responce, 'lxml')
            # block = soup.find('div', id = "holidays main")

            today = soup.find('p', style='padding: 1rem; background: #fff6e0;').find_all('span')
            for t in today:
                bot.send_message(message.chat.id, ' '.join(t.text.split()))
                #print(' '.join(t.text.split()))

            t = ''
            holidays = soup.find('ul', class_='holidays-items')
            for i in holidays:
                print(' '.join(i.text.split()[:-1]))
                t = t + (' '.join(i.text.split()[:-1])) + '\n'
            bot.send_message(message.chat.id, t)



        #@bot.message_handler(commands=['eblo'])
        #def holidays(message):
        #    bot.send_message(message.chat.id, 'Перетащите фото в чат')


        #@bot.message_handler(content_types=['photo'])
        #def face_analyze(message):

        #    try:


        #        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        #        downloaded_file = bot.download_file(file_info.file_path)

        #        src='4.jpg';
        #        with open(src, 'wb') as new_file:
        #           new_file.write(downloaded_file)
        #        bot.reply_to(message, 'Фото получено, начата обработка..')

        #    except Exception as e:
        #        bot.reply_to(message,e )



        #    try:
        #        result_dict = DeepFace.analyze(img_path='4.jpg', actions=['age', 'gender', 'race', 'emotion'])
        #        with open('face_analyze.json', 'w') as file:
        #            json.dump(result_dict, file, indent=4, ensure_ascii=False)


                # race = result_dict.get("race")
                # max_val_race = max(race.values())
                # final_dict_race = {k: v for k, v in race.items() if v == max_val_race}
                # keys_race = list(final_dict_race.keys())
                # print(f'[+] Race: {keys_race[0]}')
                #
                # emotion = result_dict.get("emotion")
                # max_val_emo = max(emotion.values())
                # final_dict_emo = {k: v for k, v in emotion.items() if v == max_val_emo}
                # keys_emo = list(final_dict_emo.keys())
                # print(f'[+] Emotions: {keys_emo[0]}')


            #     bot.send_message(message.chat.id,
            #                      f'[+] Age: {result_dict.get("age")}\n'
            #                      f'[+] Gender: {result_dict.get("gender")}\n')
            #                      # f'[+] Race: {keys_race[0]}\n'
            #                      # f'[+] Emotion: {keys_emo[0]}')
            #
            #     race = result_dict.get("race")
            #     max_val_race = max(race.values())
            #     final_dict_race = {k: v for k, v in race.items() if v == max_val_race}
            #     keys_race = list(final_dict_race.keys())
            #     print(f'[+] Race: {keys_race[0]}')
            #
            #     emotion = result_dict.get("emotion")
            #     max_val_emo = max(emotion.values())
            #     final_dict_emo = {d: h for d, h in emotion.items() if h == max_val_emo}
            #     keys_emo = list(final_dict_emo.keys())
            #     print(f'[+] Emotions: {keys_emo[0]}')
            #
            #     bot.send_message(message.chat.id,
            #             f'[+] Race: {keys_race[0]}\n'
            #             f'[+] Emotion: {keys_emo[0]}')
            #
            #
            #
            #
            #     return result_dict
            #
            # except Exception as _ex:
            #     return _ex
            #     bot.send_message(message.chat.id, f'что-то прошло не так')

        #####################################

    except Exception:
        pass




    bot.polling(none_stop=True)
