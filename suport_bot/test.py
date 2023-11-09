import telebot
from telebot import types
import logging
# from config import bot_token

logging.basicConfig(level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


import time
from datetime import date

current_date = date.today()
curr_time = time.strftime("%H:%M:%S", time.localtime())

bot_token = '6103543125:AAFlV3biYdV64ER50N4o09_47iOz5B3gRqQ'
bot = telebot.TeleBot(bot_token)

version = '0.03 alfa'
creater = '@rapot'


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='поликлиника 1', callback_data='pol1')
    btn2 = types.InlineKeyboardButton(text='поликлиника 2', callback_data='pol2')
    btn3 = types.InlineKeyboardButton(text='поликлиника 3', callback_data='pol3')
    btn4 = types.InlineKeyboardButton(text='поликлиника 4', callback_data='pol4')
    btn5 = types.InlineKeyboardButton(text='помощь', callback_data='help')
    kb.add(btn1, btn2, btn3, btn4, btn5)
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f' Привет {first_name}\n'
                                      f'выберите поликлинику, или нажмите помощь',
                     reply_markup=kb)



@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'pol1':
        print('test1')
        # cabinet = bot.send_message(callback.message.chat.id, 'напишите номер своего кабинета: ')
        # bot.register_next_step_handler(cabinet, on_click)

    elif callback.data == 'help':
        print('test2')

        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='поликлиника 1', callback_data='pol1')
        btn2 = types.InlineKeyboardButton(text='поликлиника 2', callback_data='pol2')
        btn3 = types.InlineKeyboardButton(text='поликлиника 3', callback_data='pol3')
        btn4 = types.InlineKeyboardButton(text='поликлиника 4', callback_data='pol4')
        btn5 = types.InlineKeyboardButton(text='помощь', callback_data='help')
        kb.add(btn1, btn2, btn3, btn4, btn5)

        bot.send_message(callback.message.chat.id, f' версия бота: {version}\n'
                                                   f'нажмите "добавить задачу"\n'
                                                   f'задача будет отправлена системному администратору\n'
                                                   f'после её решения Вам поступит уведомление\n'
                                                   f'по всем вопросам пишите {creater}', reply_markup=kb)

def on_click(message):
    #cabinet = message.text

    print('cabinet')
    #send = bot.send_message(message.chat.id, 'опишите проблему: ')
    #bot.register_next_step_handler(send, add_message, cabinet)



bot.infinity_polling(timeout=10, long_polling_timeout = 5)



