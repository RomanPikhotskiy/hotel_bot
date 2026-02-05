import datetime

from telebot.types import InputMediaPhoto
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from database import *
from database import CRUD
from keyboards.inline import need_photo
from loader import bot
from states.find_hotel import InfoHotel
from states.history_state import History_state


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=InfoHotel.checkInDate)
def cal(callback):
    result, key, step = DetailedTelegramCalendar().process(callback.data)

    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}",
                              callback.message.chat.id,
                              callback.message.message_id)

        with bot.retrieve_data(callback.message.chat.id) as data:

            data['fyear'] = int(result.strftime('%Y'))
            data['fmonth'] = int(result.strftime('%m'))
            data['fday'] = int(result.strftime('%d'))
        if datetime.datetime.today() <= datetime.datetime(
                year=data['fyear'], day=data['fday'], month=data['fmonth']):

            bot.set_state(callback.message.chat.id, InfoHotel.checkOutDate)
            bot.send_message(callback.message.chat.id,
                             "Введите дату выезда")
            calendar, step = DetailedTelegramCalendar().build()
            bot.send_message(callback.message.chat.id,
                             f"Select {LSTEP[step]}",
                             reply_markup=calendar)
        else:
            bot.send_message(callback.message.chat.id,
                             'Дата выезда не может быть раньше сегодняшнего дня, попробуйте еще раз')
            calendar, step = DetailedTelegramCalendar().build()
            bot.send_message(callback.message.chat.id,
                             f"Select {LSTEP[step]}",
                             reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=InfoHotel.checkOutDate)
def cal(callback):
    result, key, step = DetailedTelegramCalendar().process(callback.data)

    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}",
                              callback.message.chat.id,
                              callback.message.message_id)
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['syear'] = int(result.strftime('%Y'))
            data['smonth'] = int(result.strftime('%m'))
            data['sday'] = int(result.strftime('%d'))
        try:
            if datetime.datetime(year=data['syear'], day=data['sday'], month=data['smonth']) < datetime.datetime(
                    year=data['fyear'], day=data['fday'], month=data['fmonth']):
                raise Exception("Small")

            bot.set_state(callback.message.chat.id, InfoHotel.adults)
            bot.send_message(callback.message.chat.id, 'Сколько будет взрослых, введите число')


        except:
            bot.send_message(callback.message.chat.id,
                             'Дата выезда не может быть раньше даты заезда, попробуйте еще раз')
            calendar, step = DetailedTelegramCalendar().build()
            bot.send_message(callback.message.chat.id,
                             f"Select {LSTEP[step]}",
                             reply_markup=calendar)


@bot.callback_query_handler(func=lambda callback: True, state=InfoHotel.city)
def callback_message(callback):
    if callback.data:

        if bot.get_state(callback.message.chat.id) == 'InfoHotel:city':
            with bot.retrieve_data(callback.message.chat.id) as data:
                data['gaiaId'] = int(callback.data)
            bot.set_state(callback.message.chat.id, InfoHotel.count)
            bot.send_message(callback.message.chat.id, f"Сколько отелей показать? Введите число не больше 25")


@bot.callback_query_handler(func=lambda callback: True, state=History_state.present)
def callback_message(callback):
    CRUD.create_table()

    n = db.Hotels.select().where(db.Hotels.user_id == callback.message.chat.id,
                                 db.Hotels.number == int(callback.data))

    for x in n:

        if x.rating != '-':
            text = (
                f"Название: {x.name}\nАдрес: {x.address}\n"
                f"Стоимость проживания: {x.price}$\nРейтинг: {x.rating}⭐️\n"
                f"Оценка посетителей: {x.preview}\n"

            )
        else:
            text = (
                f"Название: {x.name}\nАдрес: {x.address}\n"
                f"Стоимость проживания: {x.price}$\n"
                f"Оценка посетителей: {x.preview}\n"

            )
        bot.set_state(callback.message.chat.id, None)
        print('теперь фотки')
        with bot.retrieve_data(callback.message.chat.id) as data:
            if data['need_photo'] == 1:
                photos = list()
                c = 0
                for photo in x.photos.split():
                    if c == 5:
                        break
                    c += 1

                    photos.append(photo)

                media = list()
                if len(photos) > 0:
                    for num, url in enumerate(photos):
                        if num == 0:
                            media.append(InputMediaPhoto(media=url, caption=text))
                        else:
                            media.append(InputMediaPhoto(media=url))
                    bot.send_media_group(callback.message.chat.id, media)
            else:
                bot.send_message(callback.message.chat.id, text)


@bot.callback_query_handler(func=lambda callback: True, state=InfoHotel.an_adult)
def callback_message(callback):
    if callback.data == 'yesa':
        bot.set_state(callback.message.chat.id, InfoHotel.adults)
        bot.send_message(callback.message.chat.id, 'Сколько будет взрослых, введите число')
    if callback.data == 'noa':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['adults'] = 0
        bot.set_state(callback.message.chat.id, InfoHotel.children)
        bot.send_message(callback.message.chat.id, 'Сколько будет детей, введите число')


@bot.callback_query_handler(func=lambda callback: True, state=InfoHotel.children)
def callback_message(callback):
    if callback.data == 'yesc':
        bot.set_state(callback.message.chat.id, InfoHotel.children)
        bot.send_message(callback.message.chat.id, 'Сколько будет детей, введите число')
    if callback.data == 'noc':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['children_count'] = 0
            data['children'] = list()

        markup = need_photo.need_photo()
        bot.set_state(callback.message.chat.id, InfoHotel.need_photo)
        bot.send_message(callback.message.chat.id, f"Нужны ли вам фотографии отелей?", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True, state=InfoHotel.need_photo)
def callback_message(callback):
    if callback.data == 'yesp':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['need_photo'] = 1
        bot.set_state(callback.message.chat.id, InfoHotel.count)
        bot.send_message(callback.message.chat.id, f"Сколько отелей показать? Введите число не больше 25")
    if callback.data == 'nop':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['need_photo'] = 0
        bot.set_state(callback.message.chat.id, InfoHotel.count)
        bot.send_message(callback.message.chat.id, f"Сколько отелей показать? Введите число не больше 25")


@bot.callback_query_handler(func=lambda callback: True, state=History_state.need_photo)
def callback_message(callback):
    if callback.data == 'yesp':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['need_photo'] = 1
    else:
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['need_photo'] = 0
    bot.set_state(callback.message.chat.id, History_state.present)
    CRUD.draw_number(callback)
