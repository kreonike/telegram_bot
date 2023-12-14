from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram import types

info = KeyboardButton(text='АДРЕСА И ТЕЛЕФОНЫ')
call = KeyboardButton(text='ВРЕМЕННО НЕДОСТУПЕНО')
spec = KeyboardButton(text='ЗАПИСЬ К ВРАЧУ')
cancel = KeyboardButton(text='ОТМЕНА ЗАПИСИ')
cancel_doctor = KeyboardButton(text='ОТМЕНА ЗАПИСИ К ВРАЧУ')
cancel_home = KeyboardButton(text='ОТМЕНА ЗАПИСИ ВЫЗОВА НА ДОМ')
checking = KeyboardButton(text='ПРОВЕРКА ЗАПИСИ')
doctor = KeyboardButton(text='информация о врачах')
woker = KeyboardButton(text='режим работы')

ther = KeyboardButton(text='ТЕРАПЕВТ')
vac = KeyboardButton(text='ВАКЦИНАЦИЯ')
dis = KeyboardButton(text='ДИСПАНСЕРИЗАЦИЯ')
sto = KeyboardButton(text='СТОМАТОЛОГ')
uro = KeyboardButton(text='УРОЛОГ')
vop = KeyboardButton(text='ВОП')
sto_ther = KeyboardButton(text='СТОМАТОЛОГ-ТЕРАПЕВТ')
xir = KeyboardButton(text='ХИРУРГ')
endo = KeyboardButton(text='ЭНДОКРИНОЛОГ')
oto = KeyboardButton(text='ОТОЛОРИНГОЛОГ')
onko = KeyboardButton(text='ОНКОЛОГ')
oftalmo = KeyboardButton(text='ОФТАЛЬМОЛОГ')

pol1 = KeyboardButton(text='ПОЛИКЛИНИКА 1')
pol2 = KeyboardButton(text='ПОЛИКЛИНИКА 2')
choise_pol2_1 = KeyboardButton(text='ПОЛ2 ул. СВОБОДЫ')
choise_pol2_2 = KeyboardButton(text='ПОЛ2 ул. ЯСНАЯ (ВОП)')

pol3 = KeyboardButton(text='ПОЛИКЛИНИКА 3')
pol4 = KeyboardButton(text='ПОЛИКЛИНИКА 4')

text = KeyboardButton(text='М')
# uro_import = KeyboardButton(text)

yes = KeyboardButton(text='ДА')
no = KeyboardButton(text='НЕТ')

menu = KeyboardButton(text='вернуться в меню')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
spec_client = ReplyKeyboardMarkup(resize_keyboard=True)
pol_client = ReplyKeyboardMarkup(resize_keyboard=True)
menu_client = ReplyKeyboardMarkup(resize_keyboard=True)
doctor_client = ReplyKeyboardMarkup(resize_keyboard=True)
ident_client = ReplyKeyboardMarkup(resize_keyboard=True)
choise_pol2 = ReplyKeyboardMarkup(resize_keyboard=True)
choise_client = ReplyKeyboardMarkup(resize_keyboard=True)

# cancel_client = ReplyKeyboardMarkup(resize_keyboard=True)

# kb_client.add(info).add(spec).add(doctor).add(woker)
# kb_client.row(info, spec, doctor, woker)
# kb_client.add(checking, spec).row(cancel, call).add(info)
kb_client.add(spec, checking).row(call, cancel).add(info)
# spec_client.add(ther, vac, dis, sto, uro, sto_ther, xir,endo,oto)
spec_client.add(menu).add(ther, sto, uro, vop, xir, endo, oto, onko, oftalmo)
pol_client.add(menu).add(pol1, pol2).row(pol3, pol4)
menu_client.add(menu)
doctor_client.add(text)
ident_client.add(menu).add(yes, no)
# choise_pol2 =
# choise_client.add(cancel_home, cancel_doctor).add(menu)
choise_client.add(cancel_doctor, cancel_home).add(menu)
