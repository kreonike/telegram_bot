import authorization
import requests

lpu_id = 'Lpu_id=2762'


def search_spec_doctor(base_ecp_spec, pol):
    print(base_ecp_spec)
    print('pol', pol)
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    if base_ecp_spec == 520101000000160:
        print('меняем специальности')
        stomat = ['520101000000160', '520101000000197', '520101000000165']

        combile_data_lpu_person_old = []
        data_lpu_person_list = []
        for i in stomat:
            search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={i}&' \
                                f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'
            print(f'  (((((((((( search_lpu_person: {search_lpu_person}')

            result_lpu_person = requests.get(search_lpu_person)
            data_lpu_person_old_ = result_lpu_person.json()
            combile_data_lpu_person_old.append(data_lpu_person_old_)
        print(f' ? combile_data_lpu_person_old: {combile_data_lpu_person_old}')
        for member in combile_data_lpu_person_old:
            for n in member['data']:
                data_lpu_person_list.append(n)

        data_lpu_person_old = data_lpu_person_list
        print(f' выход из функции data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    # if pol == '520101000000589':
    #     print('1111111111111111111111111')

    # pol1
    elif base_ecp_spec == 520101000000028 and pol == '520101000000589':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuSection_id=520101000008790&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    elif base_ecp_spec == 520101000000017 and pol == '520101000000589':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuSection_id=520101000008800&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    # pol2
    elif base_ecp_spec == 520101000000028 and pol == '520101000000591':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuSection_id=520101000007860&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    elif base_ecp_spec == 520101000000017 and pol == '520101000000591':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuSection_id=520101000007858&LpuBuilding_id=520101000000693&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    # pol3
    elif base_ecp_spec == 520101000000028 and pol == '520101000001382':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuSection_id=520101000013021&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    # pol4
    elif base_ecp_spec == 520101000000028 and pol == '520101000000181':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old


    elif base_ecp_spec == 520101000000017 and pol == '520101000000181':

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuSection_id=520101000008800&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old


    else:
        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old
