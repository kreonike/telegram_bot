# support pgonline_bot

from config import bot_token

import telebot
from telebot import types
import logging
import time
from datetime import date
#from telegram.constants import ParseMode

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

current_date = date.today()
curr_time = time.strftime("%H:%M:%S", time.localtime())

bot = telebot.TeleBot(bot_token)
group_id = '-4031621776'
user_admin = '120334532'
# tiket = 0
version = '0.01 alfa'
creater = '@rapot'


# user_id = ''


@bot.message_handler(commands=['start'])
def start(message):
    # kb = types.InlineKeyboardMarkup()
    # btn1 = types.InlineKeyboardButton(text='тарифы', callback_data='tariff')
    # btn2 = types.InlineKeyboardButton(text='задать вопрос техподдержке', callback_data='add')
    # btn3 = types.InlineKeyboardButton(text='о нас', callback_data='about')
    # kb.add(btn2, btn3, btn1)
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f' Привет, {first_name}\n'
                                      f'выберите интересующий Вас раздел ')

def menu(message):
    bot.send_message(message.chat.id, f'чтобы задать новый вопрос нажмите "задать новый вопрос"')


@bot.message_handler(commands=['add_question'])
def add_question(message):
    user = message.from_user.username
    text = message.text
    user_id = message.from_user.id

    print(user_id)
    print(message)
    question = bot.send_message(message.from_user.id, 'запишите свой вопрос: ')
    bot.register_next_step_handler(question, choise_)

def choise_(message):

    # kb = types.InlineKeyboardMarkup()
    # btn4 = types.InlineKeyboardButton(text="начать чат", callback_data='start_question')
    # btn5 = types.InlineKeyboardButton(text='завершить', callback_data='close_question')
    # kb.add(btn4, btn5)

    text = message.text
    user_id = message.from_user.id
    bot.send_message(message.chat.id, 'Ваш вопрос успешно зарегистрирован')
    bot.send_message(group_id, f'дата: {current_date}, время: {curr_time}\n'
                                      f'новый вопрос от пользователя: `{user_id}`\n'
                                      f' \n'
                                      f'{text}', parse_mode="MARKDOWN")

    bot.register_next_step_handler(message, user_chat_id)


@bot.message_handler(commands=['user_chat'])
def user_chat_id(message):
    print(message)
    print('а вот и юзер ид: ', message.from_user.id)
    bot.send_message(group_id, 'Введите user_id')
    bot.register_next_step_handler(message, chat_user_text)


def chat_user_text(message):
    message = message.text
    print(message)
    bot.send_message(group_id, f' вы ввели: {message}')

    # what = bot.send_message(group_id, 'что хотите написать')
    # print(who, what)

    #@bot.message_handler(content_types=['text'])
# def choise_(message):
#     # message = message.text
#     print('sdfsdf')
#     print(message)
    # if message == 'start_chat':
    #
    #     print('start_chat')
    #     bot.send_message(group_id, 'напишите ответ пользователю')
    #
    # elif message == 'close_question':
    #     print('close')




# @bot.callback_query_handler(func=lambda callback: callback.data)
# def choise_(callback):
#     if callback.data == 'start_question':
#
#         print('start_question', callback.data)
#         bot.send_message(group_id, 'напишите ответ пользователю')
#
#     elif callback.data == 'close_question':
#         print('close')



# @bot.message_handler(content_types=['text'])
# def question(message):
#     message = message.text
#     print(message)
        # print('!!!!!')
        # answer = bot.send_message(group_id, 'напишите ответ пользователю')
        # print(answer)

        # answer = bot.send_message(group_id, 'напишите ответ пользователю')
        # support_chat(answer)
        # # print(answer)
        # # bot.register_next_step_handler(answer, user_chat)


# def support_chat(message):
#     print(message)
#     print('test')
#     t= bot.send_message(group_id, 'напишите ответ пользователю')
#     print('это Т', t)





# @bot.message_handler(content_types=['text'])
# def user_chat(message):
#     print(message)
#     mess = message.text
#     print(mess)

bot.polling(none_stop=True, timeout=123)
