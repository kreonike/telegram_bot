import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_time(MedStaffFact_id, data_date_dict):
    print(f' получено значение в search_time1: {MedStaffFact_id}')
    print(f' получено значение в search_time2: {data_date_dict}')

    TimeTableGraf_begTime_list = []
    for key in data_date_dict['data']:
        TimeTableGraf_begTime_list.append(key['TimeTableGraf_begTime'])
    print('список дат:', TimeTableGraf_begTime_list)

    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    # TimeTableGraf_begTime_list = ['2023-11-10', '2023-11-13', '2023-11-14', '2023-11-15', '2023-11-16', '2023-11-17']
    data_time_list = []
    count = 0
    for item in TimeTableGraf_begTime_list:
        search_time = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={MedStaffFact_id}' \
                      f'&TimeTableGraf_begTime={item}&sess_id={session}'

        result_MedStaffFact_id = requests.get(search_time)
        data_time_dict = result_MedStaffFact_id.json()
        # print(data_time_dict)
        logging.info(f' data_time_dict: {data_time_dict}')

        for i in data_time_dict['data']:
            count += 1

    print(count)

    # for item in data_time_dict['data']:
    #     TimeTableGraf_id = item['TimeTableGraf_id']
    #     # logging.info(f' TimeTableGraf_id: {TimeTableGraf_id}')
    #     search_type = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafById?' \
    #                   f'TimeTableGraf_id={TimeTableGraf_id}&sess_id={session}'
    #     result_type = requests.get(search_type)
    #     data_type_dict = result_type.json()
    #     r = data_type_dict
    #     # print(f' r = {r}')
    #     for j in r['data']:
    #         if j['TimeTableType_id'] == '1' or j['TimeTableType_id'] == '4' or j['TimeTableType_id'] == '10' or j[
    #             'TimeTableType_id'] == '11':
    #             data_time_list.append(j)
    #         else:
    #             pass
    # logging.info(f' data_time_list: {data_time_dict}')
    return count
