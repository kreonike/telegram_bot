import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization
import datetime

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def entry_home(person_id, address_mess, phone_mess, reason_mess):
    print(address_mess)
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()
    # CallProfType_id
    # 1 - терапия, 2 - стоматология

    # HomeVisitCallType
    # 1 простой
    # 2 активный
    # 3 выписка рецепта
    # 4 патронаж
    # 5 вызов узкого специалиста

    KLStreet_id = '393790'
    # HomeVisit_House = '14'
    # HomeVisit_setDT = '14.11.2022 00:00'
    HomeVisitStatus_id = '1'  # назначен врач
    get_status_address = f'https://ecp.mznn.ru/api/Address?Person_id={person_id}&sess_id={session}'
    result_address = requests.get(get_status_address)
    status_address = result_address.json()
    logging.info(f' person address: {status_address}')

    # KLStreet_id = status_address['data']['1']['KLStreet_id']
    HomeVisit_House = status_address['data']['1']['Address_House']
    now = datetime.datetime.now()
    HomeVisit_setDT = now.strftime("%d.%m.%Y %H:%M")

    status_home = f'http://ecp.mznn.ru/api/HomeVisit/HomeVisit?CallProfType_id=1&' \
                  f'Address_Address={address_mess}&KLStreet_id={KLStreet_id}&HomeVisit_House={HomeVisit_House}&HomeVisitCallType_id=1&' \
                  f'HomeVisit_setDT={HomeVisit_setDT}&' \
                  f'HomeVisit_Phone={phone_mess}&HomeVisit_Symptoms={reason_mess}&' \
                  f'HomeVisitStatus_id={HomeVisitStatus_id}&HomeVisitWhoCall_id=1&Person_id={person_id}&sess_id={session}'
    result_status = requests.post(status_home)
    status_home = result_status.json()
    # logging.info(f' status_home: {status_home}')
    print(f' status_home: {status_home}')
    return status_home
