from telebot.handler_backends import State, StatesGroup


class History_state(StatesGroup):
    draw_number = State()
    need_photo = State()
    present = State()
