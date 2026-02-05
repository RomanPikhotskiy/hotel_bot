from telebot import types


def draw_num(numbers):
    markup = types.InlineKeyboardMarkup()
    buttons = list()
    b = 0
    for key in numbers:
        bt = types.InlineKeyboardButton(f"{key + 1}", callback_data=f"{key}")
        buttons.append(bt)
        b += 1
        if b == 7:
            markup.add(*buttons)
            buttons = list()

    markup.add(*buttons)
    return markup
