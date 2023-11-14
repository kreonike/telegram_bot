import telebot
from telebot import types
import logging
from config import bot_token
import search_spec_doctor
import base_ecp
import search_date
import search_time
# from kb.kb import kb_spec
# import spec_list
import search_busy_date

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

import time
from datetime import date

current_date = date.today()
curr_time = time.strftime("%H:%M:%S", time.localtime())

bot = telebot.TeleBot(bot_token)

version = '14.31 pre release'
creater = '@rapot'

# id pol
pol1 = '520101000000589'
pol2 = '520101000000591'
pol3 = '520101000001382'
pol4 = '520101000000181'

pol1_ther_LpuSection_id = '520101000008790'


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='поликлиника 1', callback_data='pol1')
    btn2 = types.InlineKeyboardButton(text='поликлиника 2', callback_data='pol2')
    btn3 = types.InlineKeyboardButton(text='поликлиника 3', callback_data='pol3')
    btn4 = types.InlineKeyboardButton(text='поликлиника 4', callback_data='pol4')
    btn5 = types.InlineKeyboardButton(text='помощь', callback_data='help')
    kb.add(btn1, btn2).add(btn3, btn4).row(btn5)
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f' Привет {first_name}\n'
                                      f'выберите поликлинику, или нажмите помощь',
                     reply_markup=kb)
    # bot.register_next_step_handler(send, serch_pol1)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'pol1':
        # print('222222', callback)
        logging.info(f' выбор пол: {callback.data}')
        serch_pol(callback)
    elif callback.data == 'pol2':
        logging.info(f' выбор пол: {callback.data}')
        serch_pol(callback)

    elif callback.data == 'pol3':
        logging.info(f' выбор пол: {callback.data}')
        serch_pol(callback)

    elif callback.data == 'pol4':
        logging.info(f' выбор пол: {callback.data}')
        serch_pol(callback)

    elif callback.data == 'help':
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='поликлиника 1', callback_data='pol1')
        btn2 = types.InlineKeyboardButton(text='поликлиника 2', callback_data='pol2')
        btn3 = types.InlineKeyboardButton(text='поликлиника 3', callback_data='pol3')
        btn4 = types.InlineKeyboardButton(text='поликлиника 4', callback_data='pol4')
        btn5 = types.InlineKeyboardButton(text='помощь', callback_data='help')
        kb.add(btn1, btn2).add(btn3, btn4).row(btn5)

        bot.send_message(callback.from_user.id, f' версия бота: {version}\n'
                                                f'по всем вопросам пишите {creater}', reply_markup=kb)


def spec_check(spec, base_ecp_medspecoms_id):
    return spec in base_ecp_medspecoms_id


def serch_pol(callback):
    # print('werwer', callback)
    choise_pol = callback.data
    if choise_pol == 'pol1':
        pol = pol1
        logging.info(f' врачи в пол: {pol}')

    elif choise_pol == 'pol2':
        pol = pol2
        logging.info(f' врачи в пол: {pol}')

    elif choise_pol == 'pol3':
        pol = pol3
        logging.info(f' врачи в пол: {pol}')

    elif choise_pol == 'pol4':
        pol = pol4
        logging.info(f' врачи в пол: {pol}')

    print(choise_pol)
    #logging.info(f' список врачей в пол: {pol}')

    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='поликлиника 1', callback_data='pol1')
    btn2 = types.InlineKeyboardButton(text='поликлиника 2', callback_data='pol2')
    btn3 = types.InlineKeyboardButton(text='поликлиника 3', callback_data='pol3')
    btn4 = types.InlineKeyboardButton(text='поликлиника 4', callback_data='pol4')
    btn5 = types.InlineKeyboardButton(text='помощь', callback_data='help')
    kb.add(btn1, btn2).add(btn3, btn4).row(btn5)

    bot.send_message(callback.from_user.id, f' ожидайте выполнения скрипта ~2min')
    logging.info(f' мы в пол: {pol}')

    base_ecp_medspecoms_id = base_ecp.medspecoms_id
    logging.info(f' специальности: {base_ecp_medspecoms_id}')

    spec = ['терапевт', 'офтальмолог', 'стоматолог', 'отоларинголог', 'хирург', 'воп', 'акушер-гинеколог']
    for spec_ in spec:
        print('spec_', spec_)

        spec_check(spec_, base_ecp_medspecoms_id)
        base_ecp_spec = base_ecp.medspecoms_id[spec_]
        logging.info(f' запрошена специальность: {base_ecp_spec}')

        data_lpu_person = search_spec_doctor.search_spec_doctor(base_ecp_spec, pol)
        logging.info(f' врачи в пол: {pol}: {data_lpu_person}')

        total_dict_base = {}
        for i in data_lpu_person:
            data_date_dict = {}
            name = i['PersonSurName_SurName']
            MedStaffFact_id = i['MedStaffFact_id']
            print(name, MedStaffFact_id)

            logging.info(f' MedStaffFact_id в пол1: {MedStaffFact_id}')
            """поиск даты"""

            data_date_dict = search_date.search_date(MedStaffFact_id)
            print(f' это дата лист из функции: {data_date_dict}')

            data_freetime = search_time.search_time(MedStaffFact_id, data_date_dict)
            print(f' data_time_final = {name} + {data_freetime}')
            data_busytime = search_busy_date.search_busy_date(MedStaffFact_id)
            print(f' data_busytime = {data_busytime}')
            # print(data_time_final.values())


            if data_freetime + data_busytime != 0:
                total_dict_base[name] = data_freetime + data_busytime
                print('total_dict_base', total_dict_base)


        spec_comparisons = '0'
        if spec_ == 'терапевт':
            spec_comparisons = 'должно быть >= 280'
            print('sdrrrrrrrrrrrrrrrrrrrrrr', spec_comparisons)

        elif spec_ == 'офтальмолог':
            spec_comparisons = 'должно быть >= 330'

        elif spec_ == 'стоматолог':
            spec_comparisons = 'должно быть >= 90'

        elif spec_ == 'отоларинголог':
            spec_comparisons = 'должно быть >= 310'

        elif spec_ == 'хирург':
            spec_comparisons = 'должно быть >= 280'

        elif spec_ == 'воп':
            spec_comparisons = 'должно быть >= 280'

        elif spec_ == 'акушер-гинеколог':
            spec_comparisons = 'должно быть >= 260'

        if not total_dict_base:
            logging.info(f' список пуст')
        else:

            # keys = list(total_dict_base.keys())
            # items = list(total_dict_base.values())
            # print(f'{keys[0]}: {items[0]}')
            print('total_dict_base!!!!!!!!!', total_dict_base)

            for i in total_dict_base:
                print(f"{i} = {total_dict_base[i]}")

            strings = []
            for key, item in total_dict_base.items():
                strings.append("{}: {}".format(key.capitalize(), item))
            result = '\n'.join(strings)
            print(result)

            bot.send_message(callback.from_user.id, f' {spec_} {spec_comparisons}\n'
                                                    f'\n'
                                                        #f'{i} = {total_dict_base[i]}')
                                                    f'{result}')

    bot.send_message(callback.from_user.id, f'выберите раздел', reply_markup=kb)




#bot.infinity_polling(timeout=10, long_polling_timeout=5)
bot.polling(none_stop=True, timeout=123)