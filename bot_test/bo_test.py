import datetime

import base_ecp
import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import bot_token, login_ecp, password_ecp
from keyboards.client_kb import kb_client, spec_client, pol_client, menu_client, ident_client

spec_dict_final = {}
MedStaffFact_id = {}
MedStaffFact_id = []
data_time_final = {}

version = '7.79 pre-release'
creator = '@rapot'

bot = Bot(bot_token)

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
    time_time = State()
    post_id = State()
    message_time = State()
    spec_dict_final = State()


# await state.finish()


# authorization
def authorization():
    login = login_ecp
    password = password_ecp
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

    # data_date_list = []

    now = datetime.datetime.now()

    tomorrow = now + datetime.timedelta(days=1)
    print(f' завтра: {tomorrow}')
    today = now.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")

    result = now + datetime.timedelta(days=6)
    TimeTableGraf_end = result.date()

    search_date = (f' https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeDate?MedStaffFact_id={MedStaffFact_id}'
                   f'&TimeTableGraf_beg={tomorrow}&TimeTableGraf_end={TimeTableGraf_end}&sess_id={session}')

    result_date = requests.get(search_date)
    data_date = result_date.json()
    print(f' data_date::: {data_date}')

    return data_date


def search_time2(MedStaffFact_id, TimeTableGraf_begTime):
    print(f' получено значение в search_time1: {MedStaffFact_id}')
    print(f' получено значение в search_time2: {TimeTableGraf_begTime}')
    TimeTableGraf_begTime = TimeTableGraf_begTime.partition(' ')[0]
    print(f' правильный: {TimeTableGraf_begTime}')

    ##авторизация
    authorization()
    session = authorization()

    # TODO тип бирки

    search_time = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={MedStaffFact_id}' \
                  f'&TimeTableGraf_begTime={TimeTableGraf_begTime}&sess_id={session}'

    result_MedStaffFact_id = requests.get(search_time)
    data_MedStaffFact_id = result_MedStaffFact_id.json()
    print(f' дата для search_time: {data_MedStaffFact_id}')

    data_time_dict = {}

    for k in data_MedStaffFact_id['data']:
        TimeTableGraf_begTime = k['TimeTableGraf_begTime']
        data_time_dict[TimeTableGraf_begTime] = k['TimeTableGraf_id']

    print(f' тут финальный словарь из search_time: {data_time_dict}')
    return data_time_dict


def search_time(MedStaffFact_id, data_date_dict):
    print(f' получено значение в search_time1: {MedStaffFact_id}')
    print(f' получено значение в search_time2: {data_date_dict}')

    TimeTableGraf_begTime_list = []
    for key in data_date_dict['data']:
        TimeTableGraf_begTime_list.append(key['TimeTableGraf_begTime'])
    print(TimeTableGraf_begTime_list)

    ##авторизация
    authorization()
    session = authorization()

    data_time_list = []
    for item in TimeTableGraf_begTime_list:

        search_time = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={MedStaffFact_id}' \
                      f'&TimeTableGraf_begTime={item}&sess_id={session}'

        result_MedStaffFact_id = requests.get(search_time)
        data_time_dict = result_MedStaffFact_id.json()
        print(data_time_dict)
        for item in data_time_dict['data']:
            TimeTableGraf_id = item['TimeTableGraf_id']
            search_type = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafById?TimeTableGraf_id={TimeTableGraf_id}&sess_id={session}'
            result_type = requests.get(search_type)
            data_type_dict = result_type.json()
            r = data_type_dict
            #print(f' r = {r}')
            for j in r['data']:
                if j['TimeTableType_id'] == '10' or j['TimeTableType_id'] == '1':
                    data_time_list.append(j)
                else:
                    pass
    return data_time_list


def check_timetabletype(data_time_final):
    pass

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


def search_double(post_id, check_entry_data, date_whithout_time):
    # check_entry_data = {'error_code': 0, 'data': {'Person_id': '7831750', 'Person_SurName': 'Соляник', 'Person_FirName': 'Дмитрий', 'Person_SecName': 'Григорьевич', 'Person_Phone': '9308000705', 'TimeTable': [{'TimeTableSource': 'Graf', 'TimeTable_id': '520101029489523', 'TimeTable_factTime': None, 'TimeTable_begTime': '2022-11-08 10:45:00', 'MedService_id': None, 'MedService_Name': None, 'MedStaffFact_id': '520101000026280', 'Post_id': '92', 'Post_name': 'Врач-эндокринолог', 'LpuSectionProfile_id': '520101000000002', 'Usluga_Code': None, 'Usluga_Name': None, 'Lpu_id': '2762'}]}}

    for j in check_entry_data['data']['TimeTable']:

        if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[
            0] == date_whithout_time:
            print('НАЙДЕНО СОВПАДЕНИЕ')
            print('запись к одному и тому же специалисту на один и тот же день запрещена')
            error = 6
            return error
        else:
            print('совпадений не найдено')
            error = 0
            return error


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


@dp.message_handler(text='вернуться в меню', state=ClientRequests.main_menu)
async def return_command(message: types.Message, state: FSMContext):
    await message.reply('выберите раздел', reply_markup=kb_client)


##кнопка возврата
menu = KeyboardButton('вернуться в меню')


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
    if mess == 'вернуться в меню':
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
    await bot.send_message(message.from_id, 'Идёт поиск, подождите ', reply_markup=menu_client)
    mess = message.text
    print(mess)

    if mess == 'вернуться в меню':
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
            await state.update_data(entry_data_delete=entry_data)

            print(f' entry_data: {entry_data}')

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
                # TODO тут было дублирование
                await bot.send_message(message.chat.id, 'Если желаете отменить запись введите ID бирки:',
                                       reply_markup=menu_client)
                await ClientRequests.entry_delete.set()  # Устанавливаем состояние

        @dp.message_handler(state=ClientRequests.entry_delete)
        async def get_delete(message: types.Message, state: FSMContext):
            message_delete = message.text
            print(f' message_delete: {message_delete}')

            if message_delete == 'вернуться в меню':
                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            elif message_delete.isdigit() == False:
                await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов',
                                    reply_markup=menu_client)
            # print(Post_name)
            # TODO тут проверить
            elif message_delete.isdigit() == True:
                data = await state.get_data()
                entry_data = data.get('entry_data_delete')
                del_status = del_entry(message_delete, entry_data)
                print(f' на выходе del_status: {del_status}')
                if del_status == '0':
                    await bot.send_message(message.chat.id, 'БИРКА УДАЛЕНА')
                    await ClientRequests.main_menu.set()  # Устанавливаем состояние
                    await bot.send_message(message.chat.id, 'выберите раздел', reply_markup=kb_client)
                    spec_dict_final = {}
                    await state.finish()  # Выключаем состояние
                elif del_status == '6':
                    await bot.send_message(message.chat.id, 'бирка не найдена, повторите ввод')




            elif message_delete == 'НЕТ':

                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                spec_dict_final = {}
                await state.finish()  # Выключаем состояние
                # await ClientRequests.next()

            else:
                await bot.send_message(message.chat.id, 'Неверный бирка, повторите попытку', reply_markup=menu_client)


def del_entry(message_delete, entry_data):
    print(message_delete)
    print(entry_data)
    del_error = ''
    for key in entry_data['data']['TimeTable']:
        if key['TimeTable_id'] == message_delete:
            print('TimeTable_id = message_delete')
            TimeTableSource = 'Graf'
            status_del = time_delete(message_delete, TimeTableSource)
            print(f' status_del: ! {status_del}')

            if status_del['data'] == []:
                print('done')
                del_error = '0'
                return del_error

        elif key['TimeTable_id'] != message_delete:
            print(f' error {del_error}')
            del_error = '6'
            print(del_error)
            return del_error


# spec_client.add(menu)
@dp.message_handler(state=ClientRequests.spec)
async def get_spec(message: types.Message, state: FSMContext):
    print(f' на входе в get_spec {spec_dict_final}')
    question_spec = message.text
    if question_spec == 'вернуться в меню':
        await ClientRequests.main_menu.set()  # Устанавливаем состояние
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.finish()  # Выключаем состояние

        print('выход тут')

    else:
        data_lpu_person = {}
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
        print(f' MedStaffFact_id data_lpu_person: {data_lpu_person}')

        global post_id

        for key in data_lpu_person['data']:
            post_id = key['Post_id']

        print(post_id)

        if data_lpu_person['data'] == []:
            await bot.send_message(message.from_id,
                                   'К данному специалисту запись на 5 ближайших дней отсутствует',
                                   reply_markup=kb_client)

        else:
            doc = ReplyKeyboardMarkup(resize_keyboard=True)
            print(spec_dict_final)
            for i in data_lpu_person['data']:
                name = i['PersonSurName_SurName']
                spec_dict_final[name] = i['MedStaffFact_id']
            print(f' ? post_id: {post_id}')
            print(f' это dict: {spec_dict_final}')

            await state.update_data(spec_dict_final=spec_dict_final)
            print(spec_dict_final)

            doc.add(menu)

            # тут создаются кнопки врачей
            for key in spec_dict_final:
                doc.add(key)
            await message.reply('К кому хотим записаться ?', reply_markup=doc)
            await ClientRequests.doctor.set()  # Устанавливаем состояние


        print(f' !! {post_id}')

        @dp.message_handler()
        async def get_doctor_name(message: types.Message, state: FSMContext):
            global spec_dict_final
            print(post_id)

            print(f't2: {spec_dict_final}')

            mess = message.text
            print(f' message_handler() mess: {mess}')

            if mess == 'вернуться в меню':
                await ClientRequests.main_menu.set()  # Устанавливаем состояние
                await message.reply('выберите раздел', reply_markup=kb_client)
                #spec_dict_final = {}
                await state.finish()  # Выключаем состояние

            else:
                await bot.send_message(message.from_id,
                                       'Идёт поиск сводных дат для записи, это может занять много времени, пожалуйста ожидайте..')
                global MedStaffFact_id

                MedStaffFact_id = (spec_dict_final[mess])
                await state.update_data(MedStaffFact_id=MedStaffFact_id)  ################

                print(f' @@ MedStaffFact_id: {MedStaffFact_id}')

                """поиск даты"""
                data_date_dict = {}
                data_date_dict = search_date(MedStaffFact_id)
                print(f' это дата лист из функции: {data_date_dict}')

                data_time_final = search_time(MedStaffFact_id, data_date_dict)
                print(f' data_time_final = {data_time_final}')

                if data_time_final == []:
                    await bot.send_message(message.from_id,
                                           'На ближажшие 6 дней нет свободных дат к данному специалисту')
                    await ClientRequests.main_menu.set()  # Устанавливаем состояние
                    await message.reply('выберите раздел', reply_markup=kb_client)
                    spec_dict_final = {}
                    await state.finish()  # Выключаем состояние

                else:
                    data_button = ReplyKeyboardMarkup(resize_keyboard=True)
                    data_button.add(menu)
                    # цикл бигелова
                    for i in data_time_final:
                        #print(i['TimeTableGraf_begTime'])
                        data_button.add(i['TimeTableGraf_begTime'])

                    await bot.send_message(message.from_id,
                                           'На ближажшие 6 дней есть следующие свободные даты:\n'
                                           'Выберите желаемую дату приёма', reply_markup=data_button)
                    await ClientRequests.time.set()  # Устанавливаем состояние

                    print(f' 1 MedStaffFact_id: {MedStaffFact_id}')

                    @dp.message_handler(state=ClientRequests.time)
                    async def get_person_time(message: types.Message, state: FSMContext):
                        message_time = message.text
                        print(f' message_time: {message_time}')
                        await state.update_data(time=message_time)

                        if message_time == 'вернуться в меню':
                            await ClientRequests.main_menu.set()  # Устанавливаем состояние
                            await message.reply('выберите раздел', reply_markup=kb_client)
                            spec_dict_final = {}
                            await state.finish()  # Выключаем состояние

                        else:
                            await bot.send_message(message.from_id, 'Идёт поиск, ожидайте:')
                            global data_time_final
                            data = await state.get_data()
                            MedStaffFact_id = data.get('MedStaffFact_id')

                            print(f' message_time в else: {message_time}')
                            data_time_final2 = search_time2(MedStaffFact_id, message_time)
                            print(f' data_time_final2: {data_time_final2}')
                            TimeTableGraf_id = data_time_final2[message_time]

                            print(f' TimeTableGraf_id !!!!!!!!: {TimeTableGraf_id}')
                            print(f' message_time: {message_time}')
                            await state.update_data(time=message_time)
                            await state.update_data(TimeTableGraf_id=TimeTableGraf_id)
                            await state.update_data(message_time=message_time)
                            # TimeTableGraf_id

                            await bot.send_message(message.from_id, 'Введите свой полис ОМС: ',
                                                   reply_markup=menu_client)
                            await ClientRequests.person.set()  # Устанавливаем состояние

                        @dp.message_handler(state=ClientRequests.person)
                        async def get_person_polis(message: types.Message, state: FSMContext):
                            message_polis = message.text
                            print(f' message_polis: {message_polis}')

                            if message_polis == 'вернуться в меню':
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


                            elif message_polis.isdigit() == True:
                                await bot.send_message(message.from_id, 'Идёт поиск, подождите ',
                                                       reply_markup=menu_client)
                                polis_data = search_polis(message_polis)
                                print(f' polis_num из функции: {polis_data}')
                                person = search_person(polis_data['data'][0]['Person_id'])
                                person_id = person['data'][0]['Person_id']
                                print(f' получена из функции: {person_id}')

                                print('=========ПРОВЕРКА=========')
                                print(f' post_id для check: {post_id}')
                                print(f' Person_id: {person_id}')
                                check_entry_data = entry_status(person_id)
                                print(check_entry_data)

                                data = await state.get_data()
                                message_time = data.get('message_time')
                                print(message_time)
                                date_whithout_time = message_time.partition(' ')[0]

                                print(post_id)
                                print(check_entry_data)
                                print(date_whithout_time)
                                global check_error
                                check_error = 0
                                for j in check_entry_data['data']['TimeTable']:
                                    if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[
                                        0] == date_whithout_time:
                                        print('НАЙДЕНО СОВПАДЕНИЕ')
                                        print('запись к одному и тому же специалисту на один и тот же день запрещена')
                                        check_error = 6

                                    else:
                                        print('совпадений не найдено')

                                print(check_error)
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

                                    if message_entry == 'вернуться в меню':
                                        print('вернуться %%%%%%% в главное меню')
                                        await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                        await message.reply('выберите раздел', reply_markup=kb_client)
                                        spec_dict_final = {}
                                        await state.finish()  # Выключаем состояние
                                        # await ClientRequests.next()

                                    elif message_entry == 'ДА':
                                        print(check_error)
                                        if check_error == 6:

                                            await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                            await message.reply(
                                                'запись к одному и тому же специалисту на один и тот же день запрещена')
                                            await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                            await message.reply('выберите раздел', reply_markup=kb_client)
                                            spec_dict_final = {}
                                            await state.finish()  # Выключаем состояние

                                        elif check_error == 0:
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
                                                                   f" ВЫ УСПЕШНО ЗАПИСАНЫ к:"
                                                                   f" {entry_data[1]['data']['TimeTable'][0]['Post_name']}"
                                                                   f" на: {entry_data[1]['data']['TimeTable'][0]['TimeTable_begTime']}\n"
                                                                   f" приходите к назначенному времени сразу к врачу,\n в регистратуру идти не нужно",
                                                                   reply_markup=menu_client)

                                            await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                            await bot.send_message(message.from_id, 'выберите раздел',
                                                                   reply_markup=kb_client)
                                            spec_dict_final = {}
                                            await state.finish()  # Выключаем состояние


                                        else:
                                            await bot.send_message(message.from_id,
                                                                   f' возникла какая-то ошибка, сообщите о пробеме @rapot'
                                                                   f' или попытайтесь позже', reply_markup=menu_client)

                                    elif message_entry == 'НЕТ':

                                        await ClientRequests.main_menu.set()  # Устанавливаем состояние
                                        await bot.send_message(message.from_id, 'выберите раздел',
                                                               reply_markup=kb_client)
                                        spec_dict_final = {}
                                        await state.finish()  # Выключаем состояние
                                        # await ClientRequests.next()



                                    else:
                                        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

                            else:
                                await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

        await state.finish()  # Выключаем состояние

    await state.finish()  # Выключаем состояние

changelog = 'реализована отмена'

#########################################################################################

# @dp.message_handler(text='информация о врачах')
# async def doctor_command(message: types.Message):
#     await message.reply('Введите фамилию доктора: ', reply_markup=menu_client)
#     await ClientRequests.doctor.set()  # Устанавливаем состояние
#
#
# @dp.message_handler(state=ClientRequests.doctor)
# async def get_doctor(message: types.Message, state: FSMContext):
#     doctor = message.text
#     d_final = doctor.lower().capitalize()
#     print(f' получено значение: {doctor}')
#     await message.reply('запрос получен, ожидайте', reply_markup=menu_client)
#     print(f' изменено на: {d_final}')
#
#     await state.update_data(doctor=d_final)
#
#     data = await state.get_data()
#     doctor = data.get('doctor')
#
#     print(doctor)
#     await ClientRequests.next()
#
#     ##################
#
#     id_fast = search_doctor(doctor)
#     print(f' получено значение из функции: {id_fast}')
#
#     try:
#         medstaffast_id = id_fast['MedStaffFact_id']
#
#     except Exception:
#         await message.reply(f' по запросу: {doctor} ничего не найдено')
#         print('какая-то ошибка')
#
#     ##авторизация
#     authorization()
#     session = authorization()
#
#     try:
#         search_lpu_doctor = f'https://ecp.mznn.ru/api/rish/MedStaffFact/getDoctorInfo?MedStaffFact_id=' \
#                             f'{medstaffast_id}&sess_id={session}'
#
#         result_lpu_doctor = requests.get(search_lpu_doctor)
#         data_lpu_doctor = result_lpu_doctor.json()
#         # print(data_lpu_doctor)
#
#         # Person_id = data_lpu_doctor['data']['Person_id']
#         doctor_fio = data_lpu_doctor['data']['doctor_fio']
#         profile_name = data_lpu_doctor['data']['profile_name']
#         lpu_nick = data_lpu_doctor['data']['lpu_nick']
#         unit_name = data_lpu_doctor['data']['unit_name']
#         LpuUnit_Address = data_lpu_doctor['data']['current_main']['LpuUnit_Address']
#         WorkData_begDate = data_lpu_doctor['data']['current_main']['WorkData_begDate']
#         Dolgnost_Name = data_lpu_doctor['data']['current_main']['Dolgnost_Name']
#         MedSpecOms_Name = data_lpu_doctor['data']['current_main']['MedSpecOms_Name']
#         LpuSection_Name = data_lpu_doctor['data']['current_main']['LpuSection_Name']
#         WorkData_begDate = data_lpu_doctor['data']['current_main']['WorkData_begDate']
#         Age = data_lpu_doctor['data']['current_main']['Age']
#         MedSpecOms_Name = data_lpu_doctor['data']['current_main']['MedSpecOms_Name']
#
#         await message.reply(f' ФИО: {doctor_fio}\n'
#                             f' возраст: {Age}\n'
#                             f' профиль: {profile_name}\n'
#                             f' специальность: {Dolgnost_Name}\n'
#                             f'ЛПУ: {lpu_nick}\n'
#                             f' место работы: {unit_name}\n'
#                             f' адрес работы: {LpuUnit_Address}\n'
#                             f' дата начала работы: {WorkData_begDate}')
#
#     except Exception:
#         pass
#         #await message.reply(f' значение1 {doctor} не найдено, повторите ввод.')
#
#     finally:
#         pass
#
#     await state.finish()  # Выключаем состояние


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

########################


# @bot.message_handler(commands=['search'])
# def handle_text(message):
#     bot.send_message(message.chat.id, "Напишите запрос вида: name surname birsday")
#
#     @bot.message_handler(content_types=['text'])
#     def handle_surname(message):
#         person = message.text
#         print(person)
#
#         list = person.split()
#
#         print(list)
#
#         if len(person.split()) == 3:
#             name = list[1]
#             surname = list[0]
#             birsday = list[2]
#             print(name, surname, birsday)
#         else:
#             print('где то ошибка')
#             # bot.send_message(message.chat.id, f' ошибка ввода')
#
#         try:
#
#             search_box = f'https://ecp.mznn.ru/api/Person?PersonSurName_SurName={surname}&PersonFirName_FirName={name}&PersonBirthDay_BirthDay={birsday}&sess_id={session}'
#
#             result = requests.get(search_box)
#             data_person = result.json()
#
#             print(f' дата персон {data_person}')
#
#             #####
#             # polic
#             ################
#
#             person_id = data_person['data'][0]['Person_id']
#             # print(person_id)
#             polic_box = f'https://ecp.mznn.ru/api/Polis?Person_id={person_id}&sess_id={session}'
#             polic = requests.get(polic_box)
#             data_polic = polic.json()
#             # print(data_polic)
#
#             #####
#             # adress
#             ###############
#             adress_box = f'https://ecp.mznn.ru/api/Address?Person_id={person_id}&sess_id={session}'
#             adress = requests.get(adress_box)
#             data_adress = adress.json()
#             print(f' адрес {data_adress}')
#
#             print(person_id)
#
#             # x = data_person
#             # PersonPhone_Phone = x['data'][0].get('PersonPhone_Phone', 'balbalba')
#             # print(PersonPhone_Phone)
#
#             PersonSurName_SurName = data_person['data'][0]['PersonSurName_SurName']
#             PersonFirName_FirName = data_person['data'][0]['PersonFirName_FirName']
#             PersonSecName_SecName = data_person['data'][0]['PersonSecName_SecName']
#             PersonBirthDay_BirthDay = data_person['data'][0]['PersonBirthDay_BirthDay']
#             Person_Sex_id = data_person['data'][0]['Person_Sex_id']
#             PersonSnils_Snils = data_person['data'][0]['PersonSnils_Snils']
#             Polis_Num = data_polic['data'][0]['Polis_Num']
#             # PersonPhone_Phone = data_person['data'][0]['PersonPhone_Phone']
#             PersonPhone_Phone = data_person['data'][0].get('PersonPhone_Phone', 'xxxx')
#             Address_Address = data_adress['data']['1']['Address_Address']
#
#             #
#             if Person_Sex_id == '1':
#                 Person_Sex_id = 'муж'
#             else:
#                 Person_Sex_id = 'жен'
#
#             bot.send_message(message.chat.id,
#                              # f' Person_id: {person_id}\n'
#                              f' Фамилия: {PersonSurName_SurName}\n'
#                              f' Имя: {PersonFirName_FirName}\n'
#                              f' Отчество: {PersonSecName_SecName}\n'
#                              f' Дата рождения: {PersonBirthDay_BirthDay}\n'
#                              f' Пол: {Person_Sex_id}\n'
#                              f' Снилс: {PersonSnils_Snils}\n'
#                              f' Полис: {Polis_Num}\n'
#                              f' Телефон: {PersonPhone_Phone}\n'
#                              f' Адресс: {Address_Address}')
#         except Exception:
#             print('где то ошибка')
#             # bot.send_message(message.chat.id, f' ошибка ввода')
#
#

##### поиск работающих врачей по специальности и месту работы, рабочий вариант


# try:
#     base_ecp_spec = base_ecp.medspecoms_id[spec]
#     print(f' базовая ид специальности: {base_ecp_spec}')
#
#     ##авторизация
#     authorization()
#     session = authorization()
#
#     search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
#                         f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'
#
#     result_lpu_person = requests.get(search_lpu_person)
#     data_lpu_person = result_lpu_person.json()
#     print(data_lpu_person)
#
#     print(f' дата id персон {data_lpu_person}')
#
#     print(f' Вы выбрали специальность: {spec}, по данной специальности работают следующие врачи: ')
#     print()
#
#     spec_dict_final = {}
#
#     print()
#
#     # lpu_persone_list = []
#
#
#
#     for i in data_lpu_person['data']:
#
#         spec_dict_final.update(
#             dict(LpuBuilding_id=i['LpuBuilding_id'], PersonSurName_SurName=i['PersonSurName_SurName']),
#             PersonFirName_FirName=i['PersonFirName_FirName'], PersonSecName_SecName=i['PersonSecName_SecName'])
#
#         print(spec_dict_final)
#
#         await message.reply(f' Место работы: {spec_dict_final.get("LpuBuilding_id")}\n'
#                             f' Имя: {spec_dict_final.get("PersonSurName_SurName")}\n'
#                             f' Фамилия: {spec_dict_final.get("PersonSurName_SurName")}\n'
#                             f' Отчество: {spec_dict_final.get("PersonSecName_SecName")}\n')
#
#
# except  Exception:
#     await message.reply(' значение {question_spec} не найдено, повторите ввод.')
#
# await state.finish()  # Выключаем состояние
