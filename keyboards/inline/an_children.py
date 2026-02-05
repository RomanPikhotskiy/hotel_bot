from telebot import types


def ans_children():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Да', callback_data='yesc'))
    markup.add(types.InlineKeyboardButton('Нет', callback_data='noc'))
    return markup
