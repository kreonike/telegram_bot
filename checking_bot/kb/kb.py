from telebot import types

kb_spec = types.InlineKeyboardMarkup()
ther = types.InlineKeyboardButton(text='ТЕРАПЕВТ', callback_data='ther')
sto = types.InlineKeyboardButton(text='СТОМАТОЛОГ', callback_data='sto')
vop = types.InlineKeyboardButton(text='ВОП', callback_data='vop')
xir = types.InlineKeyboardButton(text='ХИРУРГ', callback_data='xir')
endo = types.InlineKeyboardButton(text='ЭНДОКРИНОЛОГ', callback_data='endo')
oto = types.InlineKeyboardButton(text='ОТОЛОРИНГОЛОГ', callback_data='oto')
onko = types.InlineKeyboardButton(text='ОНКОЛОГ', callback_data='onko')
ofta = types.InlineKeyboardButton(text='ОФТАЛЬМОЛОГ', callback_data='ofta')
uro = types.InlineKeyboardButton(text='УРОЛОГ', callback_data='uro')

kb_spec.add(ther, sto, vop, xir, endo, oto, onko, ofta, uro)
