# support_task_manger_bot

from config import bot_token
from ping3 import ping
from speedtest import Speedtest

import telebot
from telebot import types
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
import time
from datetime import date


current_date = date.today()
curr_time = time.strftime("%H:%M:%S", time.localtime())

bot = telebot.TeleBot(bot_token)
group_id = '-4054447798'
tiket = 0
version = '2.05 beta'
creater = '@rapot'



@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='статус', callback_data='uptime')
    btn2 = types.InlineKeyboardButton(text='добавить задачу', callback_data='add')
    btn3 = types.InlineKeyboardButton(text='помощь', callback_data='help')
    kb.add(btn2, btn3, btn1)
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f' Привет {first_name}\n'
                                      f'нажмите кнопку "добавить задачу", чтобы добавить новую задачу',
                     reply_markup=kb)



@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'add':
        cabinet = bot.send_message(callback.from_user.id, 'напишите номер своего кабинета: ')
        bot.register_next_step_handler(cabinet, on_click)
        print('тут')

    elif callback.data == 'help':
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='статус', callback_data='uptime')
        btn2 = types.InlineKeyboardButton(text='добавить задачу', callback_data='add')
        btn3 = types.InlineKeyboardButton(text='помощь', callback_data='help')
        kb.add(btn2, btn3, btn1)

        bot.send_message(callback.from_user.id, f' версия бота: {version}\n'
                                                   f'нажмите "добавить задачу"\n'
                                                   f'задача будет отправлена системному администратору\n'
                                                   f'после её решения Вам поступит уведомление\n'
                                                   f'по всем вопросам пишите {creater}', reply_markup=kb)

    elif callback.data == 'uptime':
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='статус', callback_data='uptime')
        btn2 = types.InlineKeyboardButton(text='добавить задачу', callback_data='add')
        btn3 = types.InlineKeyboardButton(text='помощь', callback_data='help')
        kb.add(btn2, btn3, btn1)


        #$$$################

        resp_ecp = ping('ecp.mznn.ru')
        resp_m1 = ping('192.168.1.1')
        resp_m2 = ping('192.168.1.8')
        resp_m3 = ping('192.168.1.7')
        resp_m4 = ping('192.168.1.121')
        resp_c1 = ping('192.168.1.28')
        print(resp_ecp)
        print(resp_m1)
        print(resp_m2)
        print(resp_m3)
        print(resp_m4)
        print(resp_c1)

        if resp_ecp == None:
            bot.send_message(callback.message.chat.id, f' ecp.mznn.ru -->> Network Error')
        if resp_m1 == None:
            bot.send_message(callback.message.chat.id, f' floor1 server R -->> Network Error')
        if resp_m2 == None:
            bot.send_message(callback.message.chat.id, f' floor1 main R -->> Network Error')
        if resp_m3 == None:
            bot.send_message(callback.message.chat.id, f' floo4 418 serond switch-->> Network Error')
        if resp_m4 == None:
            bot.send_message(callback.message.chat.id, f' switch 4 floor -->> Network Error')
        if resp_c1 == None:
            bot.send_message(callback.message.chat.id, f' coordinator -->> Network Error')

        else:
            bot.send_message(callback.from_user.id, f' запущено тестирование сети, это может занять '
                                                       f'некоторе время, ожидайте:')

            internet = Speedtest()
            print('ожидайте завершения работы скрипта (скорость скачивания/загрузки должна быть выше: '
                          '80Mbit/s, пинг должен быть не выше 60, если это не так, пинайте меня или стаса)')
            download_speed = internet.download()
            upload_speed = internet.upload()
            ping_result = internet.results.ping

            print(f"скорость скачивания: {download_speed / 1024 / 1024:.2f}Mbit/s")
            print(f"скорость загрузки: {upload_speed / 1024 / 1024:.2f}Mbit/s")
            print(f"ping: {ping_result}ms")

            bot.send_message(callback.from_user.id, f' ecp.mznn.ru -->> Network Active\n'
                                                       f'floor1 server R -->> Network Active\n'
                                                       f'floor1 main R -->> Network Active\n'
                                                       f'floor4 418 serond switch -->> Network Active\n'
                                                       f'switch 4 floor -->> Network Active\n'
                                                       f'coordinator -->> Network Active\n'
                                                       f'\n'
                                                       f'ожидайте завершения работы скрипта (скорость скачивания/загрузки должна '
                                                       f'быть выше: 80Mbit/s, пинг должен быть не выше 60\n'
                                                       f'\n'
                                                       f'скорость скачивания: {download_speed / 1024 / 1024:.2f}Mbit/s\n'
                                                       f'скорость загрузки: {upload_speed / 1024 / 1024: .2f}Mbit/s\n'
                                                       f'ping: {ping_result}ms', reply_markup=kb)







#@bot.message_handler(commands=['menu'])
def menu(message):
    kb = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text='добавить задачу', callback_data='add')
    btn3 = types.InlineKeyboardButton(text='помощь', callback_data='help')
    kb.add(btn2, btn3)
    bot.send_message(message.chat.id, 'Если хотите добавить новую задачу'
                                      '"добавить задачу"', reply_markup=kb)


def on_click(message):
    cabinet = message.text

    print(cabinet)
    send = bot.send_message(message.chat.id, 'опишите проблему: ')
    bot.register_next_step_handler(send, add_message, cabinet)
    print(send)


def add_message(message, cabinet):
    with open('counter.txt') as counter:
        tiket = int(counter.read())
        print(tiket)

    tiket += 1

    with open('counter.txt', 'w') as counter:
        counter.write(str(tiket))
        print(tiket)

    user = message.from_user.username
    text = message.text
    user_id = message.from_user.id

    print(user_id)

    with open('requests.txt', 'a') as requests:
        requests.write(
            str(f'data: {current_date}, time: {curr_time}, user_id: {user_id}, cabinet: {cabinet}, ticket: #{tiket}, text: {text}' + '\n'))

    with open('total_requests.txt', 'a') as total_requests:
        total_requests.write(
            str(f'data: {current_date}, time: {curr_time}, user_id: {user_id}, cabinet: {cabinet}, ticket: #{tiket}, text: {text}' + '\n'))



    bot.send_message(message.chat.id, 'Ваш вопрос успешно зарегистрирован')
    bot.send_message(group_id, f' дата: {current_date}, время: {curr_time}\n'
                               f'тикет #{tiket}, от user_id: {user_id}, кабинет: {cabinet}\n'
                               f' \n'
                               f'{text}')
    menu(message)



@bot.message_handler(commands=['open'])
def open_(message):
    # tiket counter
    f = open('counter.txt', 'r')
    tiket = int(f.readline())

    f.close()

    f_stat = open('requests.txt', 'r')
    # считываем все строки
    lines = f_stat.readlines()
    print(tiket)
    # итерация по строкам
    bot.send_message(group_id, f' Всего запросов: {tiket}\n'
                               f'список запросов: ')
    for line in lines:
        print(line.strip())

        bot.send_message(group_id, line.strip())
    f_stat.close()


@bot.message_handler(commands=['stat'])
def stat(message):
    bot.send_message(group_id, f' тикетов за всё время: \n'
                               f'список запросов за всё время: ')


@bot.message_handler(commands=['close'])
def close(message):
    close_tiket = bot.send_message(group_id, f' Введите номер тикета, который хотите закрыть: ')
    print(close_tiket)
    bot.register_next_step_handler(close_tiket, delete_tickets)

import re
def delete_tickets(message):
    message = message.text

    with open('requests.txt') as requests:
        for line in requests:
            if message in line:
                logging.info(f' это искомая строка: {line}')
                send_user = line.split()
                user_id = send_user[5]
                user_name_new = user_id[:-1]
                logging.info(f' юзер, которому напишем: {user_name_new}')

                # отправка сообщения юзеру о закрытии тикета
                bot.send_message(user_name_new, 'Ваш запрос выполнен')

                bot.send_message(group_id, f' тикет: {line} будет удалён')

    str = message
    pattern = re.compile(re.escape(str))
    with open('requests.txt', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            result = pattern.search(line)
            if result is None:
                f.write(line)
            f.truncate()

#bot.polling(none_stop=True)
#bot.infinity_polling(timeout=10, long_polling_timeout = 5)
bot.polling(none_stop=True, timeout=123)
