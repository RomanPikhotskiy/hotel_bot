from telebot.handler_backends import State, StatesGroup


class InfoHotel(StatesGroup):
    city = State()
    max_cost = State()
    min_cost = State()
    checkInDate = State()
    checkOutDate = State()
    an_adult = State()
    adults = State()
    an_children = State()
    children = State()
    get_children = State()
    need_photo = State()
    count = State()
