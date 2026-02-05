from telebot import types


def ans_adult():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Да', callback_data='yesa'))
    markup.add(types.InlineKeyboardButton('Нет', callback_data='noa'))
    return markup
