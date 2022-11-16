import logging
import datetime
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_date(MedStaffFact_id):
    logging.info(f' search_date - MedStaffFact_id: {MedStaffFact_id}')
    print(f' search_date - MedStaffFact_id: {MedStaffFact_id}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    # data_date_list = []

    now = datetime.datetime.now()

    tomorrow = now + datetime.timedelta(days=1)
    print(f' завтра: {tomorrow}')
    today = now.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")

    result = now + datetime.timedelta(days=4)
    TimeTableGraf_end = result.date()

    search_date = (f' https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeDate?MedStaffFact_id={MedStaffFact_id}'
                   f'&TimeTableGraf_beg={tomorrow}&TimeTableGraf_end={TimeTableGraf_end}&sess_id={session}')

    result_date = requests.get(search_date)
    data_date = result_date.json()
    print(f' data_date::: {data_date}')

    return data_date
