# support pgonline_bot

from config import bot_token


import telebot
from telebot import types
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
import time
from datetime import date


current_date = date.today()
curr_time = time.strftime("%H:%M:%S", time.localtime())

bot = telebot.TeleBot(bot_token)
group_id = '-4031621776'
user_admin = '120334532'
#tiket = 0
version = '0.01 alfa'
creater = '@rapot'
# user_id = ''



@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='тарифы', callback_data='tariff')
    btn2 = types.InlineKeyboardButton(text='задать вопрос техподдержке', callback_data='add')
    btn3 = types.InlineKeyboardButton(text='о нас', callback_data='about')
    kb.add(btn2, btn3, btn1)
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f' Привет {first_name}\n'
                                      f'выберите интересующий Вас раздел', reply_markup=kb)



def add_question(message):

    user = message.from_user.username
    text = message.text
    user_id = message.from_user.id

    print(user_id)

    kb = types.InlineKeyboardMarkup()
    btn4 = types.InlineKeyboardButton(text="начать чат", callback_data='start_chat')

    btn5 = types.InlineKeyboardButton(text='завершить', callback_data='close_question')
    kb.add(btn4, btn5)

    bot.send_message(message.chat.id, 'Ваш вопрос успешно зарегистрирован')
    bot.send_message(group_id, f' дата: {current_date}, время: {curr_time}\n'
                               f'новый вопрос от user_id: {user_id},\n'
                               f' \n'
                               f'{text}', reply_markup=kb)
    # if callback.date == 'start_chat':
    #     print('мы начинаем чат тут')

    #bot.register_next_step_handler(user_id, add_chat)

def add_chat(message):
        message = message.text
        print('add_chat', message)





@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'add':
        question = bot.send_message(callback.from_user.id, 'запишите свой вопрос: ')
        bot.register_next_step_handler(question, add_question)
        print('тут')

    elif callback.data == 'start_chat':
        answer = bot.send_message(group_id, 'запишите свой ответ:')
        print(answer)
        #bot.register_next_step_handler(answer, add_chat)

        @bot.message_handler(content_types=['text'])
        def start_chat(message):
            print(message)





# @bot.message_handler(commands=['open'])
# def open_(message):
#     # tiket counter
#     f = open('counter.txt', 'r')
#     tiket = int(f.readline())
#
#     f.close()
#
#     f_stat = open('requests.txt', 'r')
#     # считываем все строки
#     lines = f_stat.readlines()
#     print(tiket)
#     # итерация по строкам
#     bot.send_message(group_id, f' Всего запросов: {tiket}\n'
#                                f'список запросов: ')
#     for line in lines:
#         print(line.strip())
#
#         bot.send_message(group_id, line.strip())
#     f_stat.close()


# @bot.message_handler(commands=['stat'])
# def stat(message):
#     bot.send_message(group_id, f' тикетов за всё время: \n'
#                                f'список запросов за всё время: ')
#
#
# @bot.message_handler(commands=['close'])
# def close(message):
#     close_tiket = bot.send_message(group_id, f' Введите номер тикета, который хотите закрыть: ')
#     print(close_tiket)
#     bot.register_next_step_handler(close_tiket, delete_tickets)
#
# import re
# def delete_tickets(message):
#     message = message.text
#
#     with open('requests.txt') as requests:
#         for line in requests:
#             if message in line:
#                 logging.info(f' это искомая строка: {line}')
#                 send_user = line.split()
#                 user_id = send_user[5]
#                 user_name_new = user_id[:-1]
#                 logging.info(f' юзер, которому напишем: {user_name_new}')
#
#                 # отправка сообщения юзеру о закрытии тикета
#                 bot.send_message(user_name_new, 'Ваш запрос выполнен')
#
#                 bot.send_message(group_id, f' тикет: {line} будет удалён')
#
#     str = message
#     pattern = re.compile(re.escape(str))
#     with open('requests.txt', 'r+') as f:
#         lines = f.readlines()
#         f.seek(0)
#         for line in lines:
#             result = pattern.search(line)
#             if result is None:
#                 f.write(line)
#             f.truncate()

#bot.polling(none_stop=True)
#bot.infinity_polling(timeout=10, long_polling_timeout = 5)
bot.polling(none_stop=True, timeout=123)
