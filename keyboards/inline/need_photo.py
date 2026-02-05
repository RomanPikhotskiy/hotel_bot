from telebot import types


def need_photo():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Да', callback_data='yesp'))
    markup.add(types.InlineKeyboardButton('Нет', callback_data='nop'))
    return markup
