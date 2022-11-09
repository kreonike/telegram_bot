from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

info = KeyboardButton('АДРЕСА И ТЕЛЕФОНЫ')

spec = KeyboardButton('ЗАПИСЬ К ВРАЧУ')
cancel = KeyboardButton('ОТМЕНА ЗАПИСИ')
checking = KeyboardButton('ПРОВЕРКА ЗАПИСИ')
doctor = KeyboardButton('информация о врачах')
woker = KeyboardButton('режим работы')

ther = KeyboardButton('ТЕРАПЕВТ')
vac = KeyboardButton('ВАКЦИНАЦИЯ')
dis = KeyboardButton('ДИСПАНСЕРИЗАЦИЯ')
sto = KeyboardButton('СТОМАТОЛОГ')
uro = KeyboardButton('УРОЛОГ')
vop = KeyboardButton('ВОП')
sto_ther = KeyboardButton('СТОМАТОЛОГ-ТЕРАПЕВТ')
xir = KeyboardButton('ХИРУРГ')
endo = KeyboardButton('ЭНДОКРИНОЛОГ')
oto = KeyboardButton('ОТОЛОРИНГОЛОГ')
onko = KeyboardButton('ОНКОЛОГ')
oftalmo = KeyboardButton('ОФТАЛЬМОЛОГ')

pol1 = KeyboardButton('ПОЛИКЛИНИКА 1')
pol2 = KeyboardButton('ПОЛИКЛИНИКА 2')
choise_pol2_1 = KeyboardButton('ПОЛ2 ул. СВОБОДЫ')
choise_pol2_2 = KeyboardButton('ПОЛ2 ул. ЯСНАЯ (ВОП)')

pol3 = KeyboardButton('ПОЛИКЛИНИКА 3')
pol4 = KeyboardButton('ПОЛИКЛИНИКА 4')

text = KeyboardButton('М')
# uro_import = KeyboardButton(text)

yes = KeyboardButton('ДА')
no = KeyboardButton('НЕТ')

menu = KeyboardButton('вернуться в меню')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
spec_client = ReplyKeyboardMarkup(resize_keyboard=True)
pol_client = ReplyKeyboardMarkup(resize_keyboard=True)
menu_client = ReplyKeyboardMarkup(resize_keyboard=True)
doctor_client = ReplyKeyboardMarkup(resize_keyboard=True)
ident_client = ReplyKeyboardMarkup(resize_keyboard=True)
choise_pol2 = ReplyKeyboardMarkup(resize_keyboard=True)

# cancel_client = ReplyKeyboardMarkup(resize_keyboard=True)

# kb_client.add(info).add(spec).add(doctor).add(woker)
# kb_client.row(info, spec, doctor, woker)
kb_client.add(info, spec).row(checking, cancel)
# spec_client.add(ther, vac, dis, sto, uro, sto_ther, xir,endo,oto)
spec_client.add(menu).add(ther, sto, uro, vop, xir, endo, oto, onko, oftalmo)
pol_client.add(pol1, pol2).row(pol3, pol4)
menu_client.add(menu)
doctor_client.add(text)
ident_client.add(menu).add(yes, no)
#choise_pol2 =
