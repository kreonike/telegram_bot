from datetime import date
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from contextlib import redirect_stdout

now = datetime.now()
#today = date.today()
today_sample = date.today()
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)

# Textual month, day and year
today = now.strftime('%d.%m.%Y %H:%M:%S')
today_sample = today_sample.strftime("%d.%m")

print()
# print('расписание на неделю')
print("Сегодня:", today)

session = requests.Session()

link = 'https://edu.gounn.ru/ajaxauthorize'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/75.0.3770.142 Safari/537.36'

data = {
    'username': 'rapot',
    'password': 'Jo678V2!acE@'
}

responce = session.post(link, data=data).text


print()
diary = 'https://edu.gounn.ru/journal-app/u.3426'
diary_responce = session.get(diary).text


soup = BeautifulSoup(diary_responce, 'lxml')



block = soup.find('div', id="dnevnikDays")

block_title = soup.find_all("div", {"class": "dnevnik-day__title"})
block_lesson_time = soup.find_all('div', {'class': 'dnevnik-lesson__time'})
block_day_lessons = soup.find_all('div', {'class': 'dnevnik-day__lessons'})
block_dnevnik = soup.find_all('div', {'class': 'dnevnik-lesson'})
block_mark = soup.find_all('div', {'class': 'dnevnik-mark'})



t = []

title_list = []

#for q in soup.find_all('div', {'class': 'dnevnik-lesson__time'}):
for i in soup.find_all("div", {"class": "dnevnik-day__title"}):
    title_list.append(i.text)


cleaned_list = [item.replace(' ', '') for item in title_list]
cleaned_list2 = [item.replace('\n', '') for item in cleaned_list]
cleaned_list3 = [item.replace(',', ' ') for item in cleaned_list2]
cleaned_list3.pop(0)

cleaned_list4 = [item.replace(',', ' ') for item in cleaned_list2]
cleaned_list5 = iter([item.replace(',', ' ') for item in cleaned_list3])



#cleaned_list = [item.replace(',', ' ') for item in cleaned_list2]


list_lessons = []
for o in soup.find_all('span', {'class': 'js-rt_licey-dnevnik-subject'}):
    list_lessons.append(o.text)





list_lessons2 = iter(list_lessons)



# def week_func():
#     perios_time = ''
#     week_list = []
#
#     print(cleaned_list4[0])
#
#     week_list.append(cleaned_list4[0][-5:])
#
#
#     for q in soup.find_all('div', {'class': 'dnevnik-lesson__time'}):
#
#         first_time = (q.text[0:-6])
#         if perios_time > first_time:
#             print()
#
#             next_step_title = next(cleaned_list5)
#             print(f'{next_step_title}')
#             week_list.append(next_step_title[-5:])
#
#         next_step_lesson = next(list_lessons2)
#         next_step_time = q.text
#         print(f'{next_step_time} {next_step_lesson}')
#         week_list.append(next_step_time)
#         second_time = (next_step_time[:-6])
#         perios_time = second_time
#         # list.append()
#     return week_list


# week_list = week_func()


data_dict = []


def main_func():
    perios_time = ''
    for u in soup.find_all('div', class_='dnevnik-lesson'):

        dnevnik_mark = ''

        title = soup.find_all('div', class_='dnevnik-day__title')
        # print(title)
        lesson = u.find('span', class_='js-rt_licey-dnevnik-subject').text
        lesson_time = u.find('div', class_='dnevnik-lesson__time').text
        if u.find('div', class_='dnevnik-mark'):
            dnevnik_mark = u.find('div', class_='dnevnik-mark__value').get('value')  # text.replace('\n', ''))

        data_dict.append(
            {
                # 'title': count,
                'lesson': lesson,
                'lesson_time': lesson_time,
                'dnevnik_mark': dnevnik_mark,
            }
        )
    return data_dict


main_func()

iter_title = iter(cleaned_list3)


def result_func(data_dict, iter_title):
    perios_time = ''

    print(cleaned_list4[0])

    for i in data_dict:

        first_time = (i['lesson_time'][0:-6])

        if perios_time > first_time:
            print()
            next_step_title = next(iter_title)
            print(next_step_title)

            #print(next_step_title[-5:])
            # if next_step_title[-5:] == today_sample:
            #     print('СЕГОДНЯ')




        print(f"{i['lesson_time']} {i['lesson']}, оценка: {i['dnevnik_mark']}")

        next_step_time = i['lesson_time']
        second_time = (next_step_time[:-6])
        perios_time = second_time


#result_func(data_dict, iter_title)

with open('file_name.txt', 'w') as f:
    with redirect_stdout(f):
        result_func(data_dict, iter_title)

#print('final', tt)

# print(today)
# print(today_sample)
