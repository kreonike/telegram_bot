# import telebot
# from deepface import DeepFace
import base_ecp
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards.client_kb import kb_client, spec_client, pol_client, menu_client, doctor_client, ident_client
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

spec_dict_final = {}
MedStaffFact_id = {}
MedStaffFact_id = []
# data_time_final = {}


version = '5.38 pre-release'
creator = '@rapot'
bot = Bot("")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def shutdown(dp):
    await storage.close()
    await bot.close()


class ClientRequests(StatesGroup):
    spec = State()
    doctor = State()
    menu = State()
    pol = State()
    doctor = State()
    doctor_name = State()
    time = State()
    person = State()
    date = State()
    polic = State()
    entry = State()
    TimeTableGraf_id = State()
    person_id = State()
    main_menu = State()
    cancel = State()
    entry_delete = State()
    MedStaffFact_id = State()
    checking = State()


# authorization
def authorization():
    login = ''
    password = ''
    link = 'https://ecp.mznn.ru/api/user/login' + '?Login=' + login + '&Password=' + password

    responce = requests.get(link)
    data_session = responce.json()
    session = data_session['sess_id']

    return session


def search_date(MedStaffFact_id):
    print(f' search_date - MedStaffFact_id: {MedStaffFact_id}')
    ##авторизация
    authorization()
    session = authorization()

    data_date_list = []

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    result = now + datetime.timedelta(days=5)
    TimeTableGraf_end = result.date()
    search_date = (f' https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeDate?MedStaffFact_id={MedStaffFact_id}'
                   f'&TimeTableGraf_beg={today}&TimeTableGraf_end={TimeTableGraf_end}&sess_id={session}')

    result_date = requests.get(search_date)
    data_date = result_date.json()
    print(f' data_date::: {data_date}')
    for k in data_date['data']:
        data_date_list.append(k['TimeTableGraf_begTime'])
    print(data_date)

    return data_date


def search_time(MedStaffFact_id, TimeTableGraf_begTime):
    print(f' получено значение в search_time1: {MedStaffFact_id}')
    print(f' получено значение в search_time2: {TimeTableGraf_begTime}')

    ##авторизация
    authorization()
    session = authorization()

    search_time = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={MedStaffFact_id}' \
                  f'&TimeTableGraf_begTime={TimeTableGraf_begTime}&sess_id={session}'

    result_MedStaffFact_id = requests.get(search_time)
    data_MedStaffFact_id = result_MedStaffFact_id.json()
    print(f' дата для search_time: {data_MedStaffFact_id}')

    data_time_dict = {}

    for k in data_MedStaffFact_id['data']:
        # print(k)
        TimeTableGraf_begTime = k['TimeTableGraf_begTime']
        data_time_dict[TimeTableGraf_begTime] = k['TimeTableGraf_id']

    print(f' тут финальный словарь из search_time: {data_time_dict}')
    return data_time_dict


def search_polis(polis):
    print(f' получен полис в функцию search_polis: {polis}')
    ##авторизация
    authorization()
    session = authorization()

    search_polis = f'https://ecp.mznn.ru/api/Polis?Polis_Num={polis}&sess_id={session}'
    result_polis = requests.get(search_polis)
    polis_data = result_polis.json()
    print(f' дата для search_time: {polis_data}')
    return polis_data


def search_person(person_id):
    print(f' получен person_id в функцию search_person: {person_id}')
    ##авторизация
    authorization()
    session = authorization()

    search_person = f'https://ecp.mznn.ru/api/Person?Person_id={person_id}&sess_id={session}'
    result_person = requests.get(search_person)
    person_data = result_person.json()
    print(f' дата в person_id: {person_data}')
    return person_data


def search_entry(person_id, TimeTableGraf_id):
    print(f' в функцию search_entry получен {person_id}')
    ##авторизация
    authorization()
    session = authorization()

    ##сама запись post запрос
    search_entry = f'https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafWrite?Person_id={person_id}&TimeTableGraf_id={TimeTableGraf_id}&sess_id={session}'
    result_entry = requests.post(search_entry)
    entry_date = result_entry.json()

    # print(entry_date)

    ##статус бирки
    status_entry = f'https://ecp.mznn.ru/api/TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'
    result_status = requests.get(status_entry)
    status_date = result_status.json()

    # print(status_date)

    return entry_date, status_date


def entry_status(person_id):
    ##авторизация
    authorization()
    session = authorization()

    ##статус бирки
    status_entry = f'https://ecp.mznn.ru/api/TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'
    result_status = requests.get(status_entry)
    status_date = result_status.json()
    # print(status_date)
    return status_date


def time_delete(TimeTable_id, TimeTableSource):
    ##авторизация
    authorization()
    session = authorization()
    print(f' TimeTableSource: {TimeTableSource}')
    FailCause = 1
    ##удаляем бирку
    delete_time = f'https://ecp.mznn.ru/api/TimeTable?TimeTable_id={TimeTable_id}&TimeTableSource={TimeTableSource}&FailCause={FailCause}&sess_id={session}'
    result_detele = requests.delete(delete_time)
    status_delete = result_detele.json()
    print(f' status_delete::: {status_delete}')
    if status_delete['error_code'] == 6:  # or status_delete['error_code'] != 0:
        print('Бирка не найдена в системе.')
        error = 6
        return error
    else:
        return status_delete


def search_doctor(d_final):
    fast_id = base_ecp.medspecoms_id.values()
    print(f' передано значение: {d_final}')

    ###мне вот эта конструкция не нравится

    id_fast = 1

    ###############################

    ##авторизация
    authorization()
    session = authorization()

    for i in fast_id:
        search_fast_id = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={i}&' \
                         f'{lpu_id}&sess_id={session}'

        result_fast_id = requests.get(search_fast_id)
        data_fast_id = result_fast_id.json()

        for k in data_fast_id['data']:
            if d_final == k['PersonSurName_SurName']:
                id_fast = k
            else:
                pass
    return id_fast


# некоторые переменные
####

lpu_id = 'Lpu_id=2762'


####

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        f' Добро пожаловать,\n'
        f' я бот помошник по ГБУЗ НО ГКБ №12\n'
        f' г.Нижний Новгород, Мочалова, д.8\n'
        f' для получения информации оспользуйтесь кнопками внизу\n'
        f' замечания и предложения: {creator}\n'
        f'\n'
        f' версия бота: {version}\n', reply_markup=kb_client)


@dp.message_handler(text='вернуться в главное меню', state=ClientRequests.main_menu)
async def return_command(message: types.Message, state: FSMContext):
    await message.reply('выберите раздел', reply_markup=kb_client)


##кнопка возврата
menu = KeyboardButton('вернуться в главное меню')


@dp.message_handler(commands=['help'], state=None)
async def help_command(message: types.Message):
    await message.answer(version)


@dp.message_handler(text='АДРЕСА И ТЕЛЕФОНЫ', state=None)
async def info_command(message: types.Message):
    await message.answer(
        f' CТАЦИОНАР ГКБ12\n'
        f' Нижний Новгородул, ул. Павла Мочалова,8\n'
        f' Секретарь: 273-00-62\n'
        f'\n'
        f' ПОЛИКЛИНИКА №1\n'
        f' Нижний Новгород, ул.Васенко,11\n'
        f' регистратура: 280-85-95\n'
        f'\n'
        f' ПОЛИКЛИНИКА №2\n'
        f' Нижний Новгород, ул.Свободы, 3\n'
        f' регистратура: 273-03-00\n'
        f'\n'
        f' ПОЛИКЛИНИКА №3\n'
        f' Нижний Новгород, ул.Циолковского,9\n'
        f' Регистратура 225-01-87\n'
        f'\n'
        f' ПОЛИКЛИНИКА №4\n'
        f' Светлоярская улица, 38А'
        f' регистратура: 271-89-72', reply_markup=kb_client)


@dp.message_handler(text='режим работы', state=None)
async def woker_command(message: types.Message):
    await message.answer(
        f' Стационар ГБК12\n'
        f' круглосуточно\n'
        f'\n'
        f' Поликлиника №1\n'
        f' пн-пт 7:30-19:30\n'
        f' сб-вс 08.30-14.30\n'
        f'\n'
        f' Поликлиника №2\n'
        f' пн-пт 7:30-19:30\n'
        f' \n'
        f' Поликлиника №3\n'
        f' пн-пт 7:30-19:00\n'
        f' сб-вс 08:00-14:00'
        f'\n'
        f' Поликлиника №4\n'
        f' пн-пт 7:30-19:30', reply_markup=kb_client)


@dp.message_handler(commands=['entry'], state=None)
async def write_command(message: types.Message):
    await message.answer(version, reply_markup=kb_client)


@dp.message_handler(text='ЗАПИСЬ К ВРАЧУ')
async def spec_command(message: types.Message):
    @dp.message_handler(text='ПОЛИКЛИНИКА 1')
    async def spec_command(message: types.Message, state: FSMContext):
        print('поликлиника 1')
        await state.update_data(pol='520101000000589')

        await message.reply('Выберите специальность', reply_markup=spec_client)
        await ClientRequests.spec.set()  # Устанавливаем состояние

    @dp.message_handler(text='ПОЛИКЛИНИКА 2')
    async def spec_command(message: types.Message, state: FSMContext):
        print('поликлиника 2')
        await state.update_data(pol='520101000000591')

        await message.reply('Выберите специальность', reply_markup=spec_client)
        await ClientRequests.spec.set()  # Устанавливаем состояние

    @dp.message_handler(text='ПОЛИКЛИНИКА 3')
    async def spec_command(message: types.Message, state: FSMContext):
        print('поликлиника 3')
        await state.update_data(pol='520101000001382')

        await message.reply('Выберите специальность', reply_markup=spec_client)
        await ClientRequests.spec.set()  # Устанавливаем состояние

    @dp.message_handler(text='ПОЛИКЛИНИКА 4')
    async def spec_command(message: types.Message, state: FSMContext):
        print('поликлиника 4')
        await state.update_data(pol='520101000000591')

        await message.reply('Выберите специальность', reply_markup=spec_client)
        await ClientRequests.spec.set()  # Устанавливаем состояние

    await message.reply('Выберите поликлинику', reply_markup=pol_client)


@dp.message_handler(text='ПРОВЕРКА ЗАПИСИ', state=None)
async def cancel_command(message: types.Message):
    await bot.send_message(message.from_id, 'Введите свой полис ОМС: ', reply_markup=menu_client)
    await ClientRequests.checking.set()  # Устанавливаем состояние


@dp.message_handler(state=ClientRequests.checking)
async def checking(message: types.Message, state: FSMContext):
    mess = message.text
    print(mess)

    if mess == 'вернуться в главное меню':
        print('+вернуться в главное меню+')
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.finish()

    elif mess.isdigit() == False:
        await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов')

    elif len(mess) != 16:
        await message.reply('Неверный ввод, введите 16 цифр номера полиса')

    else:

        print('отмена')
        polis_data = search_polis(mess)
        print(polis_data)

        if polis_data['data'] == []:
            print('такого полиса не существует')
            await message.reply('Неверный ввод, такого полиса не существует')
        else:

            print(polis_data['data'][0]['Polis_id'])
            person_data = search_person(polis_data['data'][0]['Person_id'])
            print(person_data)
            person_id = person_data['data'][0]['Person_id']
            entry_data = entry_status(person_id)

            print(f' entry_ data: {entry_data}')

            if entry_data['data']['TimeTable'] == []:
                print('ничего нет')
                await bot.send_message(message.chat.id, 'ЗАПИСЕЙ НА ПРИЁМ НЕ НАЙДЕНО')
                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            else:
                for key in entry_data['data']['TimeTable']:
                    name = key['Post_name']
                    time = key['TimeTable_begTime']
                    id = key['TimeTable_id']
                    await bot.send_message(message.chat.id, f' ВЫ ЗАПИСАНЫ к: {name}\n на: {time}\n')
                    await bot.send_message(message.chat.id, f" ID бирки: `{id}`", parse_mode="Markdown")
                    await ClientRequests.main_menu.set()  # Устанавливаем состояние
                    await bot.send_message(message.chat.id, 'выберите раздел', reply_markup=kb_client)
                    spec_dict_final = {}
                    await state.finish()  # Выключаем состояние


@dp.message_handler(text='ОТМЕНА ЗАПИСИ', state=None)
async def cancel_command(message: types.Message):
    await bot.send_message(message.from_id, 'Введите свой полис ОМС: ', reply_markup=menu_client)
    await ClientRequests.cancel.set()  # Устанавливаем состояние


@dp.message_handler(state=ClientRequests.cancel)
async def checking(message: types.Message, state: FSMContext):
    mess = message.text
    print(mess)

    if mess == 'вернуться в главное меню':
        print('+вернуться в главное меню+')
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.finish()

    elif mess.isdigit() == False:
        await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов')

    elif len(mess) != 16:
        await message.reply('Неверный ввод, введите 16 цифр номера полиса')

    else:

        print('отмена')
        polis_data = search_polis(mess)
        print(polis_data)

        if polis_data['data'] == []:
            print('такого полиса не существует')
            await message.reply('Неверный ввод, такого полиса не существует')
        else:

            print(polis_data['data'][0]['Polis_id'])
            person_data = search_person(polis_data['data'][0]['Person_id'])
            print(person_data)
            person_id = person_data['data'][0]['Person_id']
            entry_data = entry_status(person_id)

            print(f' entry_data: {entry_data}')

            if entry_data['data']['TimeTable'] == []:
                print('ничего нет')
                await bot.send_message(message.chat.id, 'ЗАПИСЕЙ НА ПРИЁМ НЕ НАЙДЕНО')
                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            else:
                # person_id_delete = ['data']['Person_id']
                for key in entry_data['data']['TimeTable']:
                    name = key['Post_name']
                    time = key['TimeTable_begTime']
                    id = key['TimeTable_id']
                    await bot.send_message(message.chat.id, f' ВЫ ЗАПИСАНЫ к: {name}\n на: {time}\n')
                    await bot.send_message(message.chat.id, f" ID бирки: `{id}`", parse_mode="Markdown")

                    await bot.send_message(message.chat.id, 'Если желаете отменить запись введите ID бирки:',
                                           reply_markup=menu_client)
                    await ClientRequests.entry_delete.set()  # Устанавливаем состояние

        @dp.message_handler(state=ClientRequests.entry_delete)
        async def get_delete(message: types.Message, state: FSMContext):
            message_delete = message.text
            print(f' message_delete: {message_delete}')

            if message_delete == 'вернуться в главное меню':
                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            elif message_delete.isdigit() == False:
                await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов',
                                    reply_markup=menu_client)


            elif message_delete.isdigit() == True:

                for key in entry_data['data']['TimeTable']:
                    if key['TimeTable_id'] != message_delete:
                        await message.reply('Данная бирка Вам не принадлежит, удаление невозможно',
                                            reply_markup=menu_client)
                    else:

                        TimeTableSource = 'Graf'
                        status_del = time_delete(message_delete, TimeTableSource)
                        print(status_del)
                        print(status_del)

                        if status_del['data'] == []:
                            print('done')
                            await bot.send_message(message.chat.id, 'ЗАПИСЬ К ВРАЧУ УДАЛЕНА', reply_markup=menu_client)

                            await ClientRequests.main_menu.set()  # Устанавливаем состояние
                            await message.reply('выберите раздел', reply_markup=kb_client)
                            spec_dict_final = {}
                            await state.finish()  # Выключаем состояние




            elif message_delete == 'НЕТ':

                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            else:
                await bot.send_message(message.chat.id, 'Неверный ввод, повторите попытку', reply_markup=menu_client)


@dp.message_handler(state=ClientRequests.spec)
async def get_spec(message: types.Message, state: FSMContext):
    question_spec = message.text
    if question_spec == 'вернуться в главное меню':
        await ClientRequests.main_menu.set()  # Устанавливаем состояние
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.finish()  # Выключаем состояние

        print('выход тут')

    else:
        spec_final = question_spec.lower()
        print(f' получено значение: {question_spec}')
        print(f' изменено на: {spec_final}')

        await state.update_data(spec=spec_final)

        data = await state.get_data()
        spec = data.get('spec')
        pol = data.get('pol')

        print(f' spec = {spec}')
        print(f' pol = {pol}')
        await ClientRequests.next()

        base_ecp_spec = base_ecp.medspecoms_id[spec]
        print(f' базовая ид специальности: {base_ecp_spec}')

        ##авторизация
        authorization()
        session = authorization()

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person = result_lpu_person.json()
        print(data_lpu_person)
        if data_lpu_person['data'] == []:
            await bot.send_message(message.from_id,
                                   'К данному специалисту запись на 5 ближайших дней отсутствует',
                                   reply_markup=kb_client)

        else:
            doc = ReplyKeyboardMarkup(resize_keyboard=True)
            for i in data_lpu_person['data']:
                name = i['PersonSurName_SurName']
                spec_dict_final[name] = i['MedStaffFact_id']

            print(f' это dict: {spec_dict_final}')
            doc.add(menu)

            for key in spec_dict_final:
                doc.add(key)

            await message.reply('К кому хотим записаться ?', reply_markup=doc)
            await ClientRequests.doctor.set()  # Устанавливаем состояние

        @dp.message_handler()
        async def get_doctor_name(message: types.Message, state: FSMContext):
            await bot.send_message(message.from_id, 'Идёт поиск сводных дат для записи, ожидайте..')
            global spec_dict_final
            print(f't2: {spec_dict_final}')
            mess = message.text
            print(f' message_handler() mess: {mess}')
            if mess == 'вернуться в главное меню':
                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            else:
                global MedStaffFact_id
                MedStaffFact_id = (spec_dict_final[mess])
                await state.update_data(MedStaffFact_id=MedStaffFact_id)  ################

                print(f' @@ MedStaffFact_id: {MedStaffFact_id}')

                """поиск даты"""
                data_date_list = []
                search_date(MedStaffFact_id)
                data_date_list = search_date(MedStaffFact_id)
                print(f' это дата лист из функции: {data_date_list}')

                data_button = ReplyKeyboardMarkup(resize_keyboard=True)
                data_button.add(menu)

                TimeTableGraf_begTime = []
                ### цикл бигелова
                for key in data_date_list['data']:
                    print(key['TimeTableGraf_begTime'])
                    data_button.add(key['TimeTableGraf_begTime'])
                    TimeTableGraf_begTime.append(key['TimeTableGraf_begTime'])

                ## без вот этой хуйни не работает, обнуляю словарь тут.
                spec_dict_final = {}
                print(f' это список TimeTableGraf_begTime: {TimeTableGraf_begTime}')
                if TimeTableGraf_begTime == []:
                    await bot.send_message(message.from_id,
                                           'На ближажшие 5 дней нет свободных дат к данному специалисту')
                    await ClientRequests.main_menu.set()  # Устанавливаем состояние
                    await message.reply('выберите раздел', reply_markup=kb_client)
                    spec_dict_final = {}
                    await state.finish()  # Выключаем состояние

                else:
                    await bot.send_message(message.from_id,
                                           'На ближажшие 5 дней есть следующие свободные даты:\n'
                                           'Выберите желаемую дату приёма', reply_markup=data_button)
                    await ClientRequests.date.set()  # Устанавливаем состояние

                @dp.message_handler(state=ClientRequests.date)
                async def time(message: types.Message, state: FSMContext):
                    spec_dict_final = {}
                    print('sdfffffffffffff')
                    time_mess = message.text
                    print(f' time_mess: {time_mess}')

                    """передать TimeTableGraf_begTime и MedStaffFact_id (он выше по коду в переменной)"""

                    print(f' TimeTableGraf_begTime: {time_mess}')
                    print(f' MedStaffFact_id: {MedStaffFact_id}')

                    if time_mess == 'вернуться в главное меню':
                        await ClientRequests.main_menu.set()  # Устанавливаем состояние
                        await message.reply('выберите раздел', reply_markup=kb_client)
                        spec_dict_final = {}
                        await state.finish()  # Выключаем состояние

                    else:
                        data_time_final = search_time(MedStaffFact_id, time_mess)
                        print(f' !!!!!!! data_time_final{data_time_final}')

                        await ClientRequests.next()

                        """создание кнопок time"""
                        data_time = ReplyKeyboardMarkup(resize_keyboard=True)
                        data_time.add(menu)

                        for key_time in data_time_final:
                            print(f' время: {key_time}')
                            data_time.add(key_time)

                        await bot.send_message(message.from_id, 'Выберите желаемое время приёма:',
                                               reply_markup=data_time)

                    @dp.message_handler(state=ClientRequests.time)
                    async def get_person_time(message: types.Message, state: FSMContext):
                        message_time = message.text
                        print(f' message_time: {message_time}')

                        if message_time == 'вернуться в главное меню':
                            await ClientRequests.main_menu.set()  # Устанавливаем состояние
                            await message.reply('выберите раздел', reply_markup=kb_client)
                            spec_dict_final = {}
                            await state.finish()  # Выключаем состояние

                        else:
                            data = await state.get_data()
                            MedStaffFact_id = data.get('MedStaffFact_id')

                            data_time_final = search_time(MedStaffFact_id, time_mess)
                            print(f' data_time_final в else: {data_time_final}')
                            print(f' message_time в else: {message_time}')
                            TimeTableGraf_id = data_time_final[message_time]
                            print(f' TimeTableGraf_id !!!!!!!!: {TimeTableGraf_id}')
                            print(f' message_time: {message_time}')
                            await state.update_data(time=message_time)
                            await state.update_data(TimeTableGraf_id=TimeTableGraf_id)

                            await bot.send_message(message.from_id, 'Введите свой полис ОМС: ',
                                                   reply_markup=menu_client)
                            await ClientRequests.person.set()  # Устанавливаем состояние

                        @dp.message_handler(state=ClientRequests.person)
                        async def get_person_polis(message: types.Message, state: FSMContext):
                            message_polis = message.text
                            print(f' message_polis: {message_polis}')

                            if message_polis == 'вернуться в главное меню':
                                print('@@вернуться в главное меню')
                                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                await message.reply('выберите раздел', reply_markup=kb_client)
                                spec_dict_final = {}
                                await state.finish()  # Выключаем состояние

                            elif len(message_polis) != 16:
                                await message.reply('Неверный ввод, введите 16 цифр номера полиса',
                                                    reply_markup=menu_client)

                            elif message_polis.isdigit() == False:
                                await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов',
                                                    reply_markup=menu_client)

                            else:

                                print(f' message_polic: {message_polis}')
                                polis_data = search_polis(message_polis)
                                print(f' polis_num из функции: {polis_data}')
                                person = search_person(polis_data['data'][0]['Person_id'])
                                person_id = person['data'][0]['Person_id']

                                print(f' получена из функции: {person_id}')
                                await state.update_data(person_id=person_id)

                                PersonSurName_SurName = person['data'][0]['PersonSurName_SurName']
                                PersonFirName_FirName = person['data'][0]['PersonFirName_FirName']
                                PersonSecName_SecName = person['data'][0]['PersonSecName_SecName']
                                PersonBirthDay_BirthDay = person['data'][0]['PersonBirthDay_BirthDay']

                                await message.reply(
                                    f' Фамилия: {PersonSurName_SurName}\n'
                                    f' Имя: {PersonFirName_FirName}\n'
                                    f' Отчество: {PersonSecName_SecName}\n'
                                    f' Дата рождения: {PersonBirthDay_BirthDay}\n')

                                await bot.send_message(message.from_id, 'Это Вы ?', reply_markup=ident_client)

                                await ClientRequests.entry.set()  # Устанавливаем состояние

                                @dp.message_handler(state=ClientRequests.entry)
                                async def get_person(message: types.Message, state: FSMContext):
                                    message_entry = message.text
                                    print(message_entry)

                                    if message_entry == 'вернуться в главное меню':
                                        print('вернуться %%%%%%% в главное меню')
                                        await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                        await message.reply('выберите раздел', reply_markup=kb_client)
                                        spec_dict_final = {}
                                        await state.finish()  # Выключаем состояние

                                    if message_entry == 'ДА':
                                        data = await state.get_data()
                                        time = data.get('time')
                                        TimeTableGraf_id = data.get('TimeTableGraf_id')
                                        person_id = data.get('person_id')

                                        print(f' message_time: {time}')
                                        print(f' TimeTableGraf_id: {TimeTableGraf_id}')
                                        print(f' person_id: {person_id}')

                                        entry_data = search_entry(person_id, TimeTableGraf_id)
                                        print(f' entry_data: {entry_data}')

                                        await bot.send_message(message.from_id,
                                                               f" ВЫ УСПЕШНО ЗАПИСАНЫ к: {entry_data[1]['data']['TimeTable'][0]['Post_name']}"
                                                               f" на: {entry_data[1]['data']['TimeTable'][0]['TimeTable_begTime']}",
                                                               reply_markup=menu_client)

                                        await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                        await bot.send_message(message.from_id, 'выберите раздел',
                                                               reply_markup=kb_client)
                                        spec_dict_final = {}
                                        await state.finish()  # Выключаем состояние



                                    elif message_entry == 'НЕТ':

                                        await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                        await message.reply('выберите раздел', reply_markup=kb_client)
                                        spec_dict_final = {}
                                        await state.finish()  # Выключаем состояние

                                    else:
                                        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

        await state.finish()  # Выключаем состояние


changelog = 'реализована отмена'

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
