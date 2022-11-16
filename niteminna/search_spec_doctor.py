import authorization
import requests

lpu_id = 'Lpu_id=2762'


def search_spec_doctor(base_ecp_spec, pol):
    print(base_ecp_spec)
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    if base_ecp_spec == 520101000000160:
        print('меняем специальности')
        stomat = ['520101000000160', '520101000000197', '520101000000165']

        combile_data_lpu_person_old = []
        data_lpu_person_list = []
        for i in stomat:
            # print(i)
            search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={i}&' \
                                f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'
            print(f'  (((((((((( search_lpu_person: {search_lpu_person}')

            result_lpu_person = requests.get(search_lpu_person)
            # data_lpu_person_old.append(result_lpu_person.json())
            data_lpu_person_old_ = result_lpu_person.json()
            # print(data_lpu_person_old_)
            combile_data_lpu_person_old.append(data_lpu_person_old_)
        print(f' ? combile_data_lpu_person_old: {combile_data_lpu_person_old}')
        for member in combile_data_lpu_person_old:
            for n in member['data']:
                data_lpu_person_list.append(n)
                # print(n)

        # print(f' data_lpu_person_old в цикле: {data_lpu_person_old}')
        # data_lpu_person_old = data_lpu_person_old['data']
        # print(f' data_lpu_person_old на выходе из цикла: {data_lpu_person_old}')
        # print(data_lpu_person_old['data'])
        data_lpu_person_old = data_lpu_person_list
        print(f' выход из функции data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old

    else:

        search_lpu_person = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={base_ecp_spec}&' \
                            f'{lpu_id}&LpuBuilding_id={pol}&sess_id={session}'

        result_lpu_person = requests.get(search_lpu_person)
        data_lpu_person_old_ = result_lpu_person.json()
        data_lpu_person_old = data_lpu_person_old_['data']

        print(f' MedStaffFact_id data_lpu_person_old: {data_lpu_person_old}')
        return data_lpu_person_old
