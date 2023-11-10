import logging
import datetime
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_busy_date(MedStaffFact_id):
    logging.info(f' search_busy date - MedStaffFact_id: {MedStaffFact_id}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    now = datetime.datetime.now()

    tomorrow = now + datetime.timedelta(days=1)

    # today = now.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    logging.info(f' tomorrow: {tomorrow}')

    result = now + datetime.timedelta(days=15)
    TimeTableGraf_end = result.date()
    logging.info(f' TimeTableGraf_end: {TimeTableGraf_end}')

    search_date = (
        f' https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafByMedStaffFact?MedStaffFact_id={MedStaffFact_id}'
        f'&TimeTableGraf_beg={tomorrow} 00:00:00&TimeTableGraf_end={TimeTableGraf_end} 00:00:00&sess_id={session}')
    # print(search_date)

    result_busy_date = requests.get(search_date)
    data_busy_date = result_busy_date.json()
    print(f' data_date::: {data_busy_date}')
    busy_counter = 0
    for i in data_busy_date['data']:
        busy_counter += 1
    print(busy_counter)

    return busy_counter

# MedStaffFact_id = 520101000080716
# search_busy_date(MedStaffFact_id)
