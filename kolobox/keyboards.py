from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Комедия')],
    [KeyboardButton(text='Драма')],
    [KeyboardButton(text='Фантастика')]
],
                    resize_keyboard=True,
                    input_field_placeholder='Выберите пункт меню.')