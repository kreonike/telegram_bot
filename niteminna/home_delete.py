import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization
import datetime

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def home_delete(homevisit_id):
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    try:
        get_status_address = f'https://ecp.mznn.ru/api/HomeVisit/HomeVisitCancel?HomeVisit_id=' \
                             f'{homevisit_id}&sess_id={session}'

        result_address = requests.put(get_status_address)
        status_address = result_address.json()
        print(status_address)

        return status_address
    except TypeError:
        print('дата пустое')
