from telebot.types import Message, InputMediaPhoto
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from api import api
from keyboards.inline import an_children
from keyboards.inline import need_photo
from states.find_hotel import InfoHotel
import re
from database import CRUD
import urllib.request
from loader import bot
import logging

logging.basicConfig(filename="py_log.log")


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_city(message: Message) -> None:
    bot.set_state(message.from_user.id, InfoHotel.city, message.chat.id)
    with bot.retrieve_data(message.chat.id) as data:
        data['command'] = message.text
        data['sort'] = 'price'
        if message.text == '/bestdeal':
            data['sort'] = 'distance'
    bot.send_message(message.from_user.id, f"Введите название города, в котором хотите найти отель латиницей")


@bot.message_handler(state=InfoHotel.city)
def get_city(message: Message) -> None:
    try:
        with bot.retrieve_data(message.chat.id) as data:
            data['City'] = message.text
        if "".join(message.text.strip().split()).isalpha():
            answer = api.locations_search(message.text.strip())
            if str(answer) == ("{'message': 'You have exceeded the MONTHLY quota for requests on your current plan, "
                               "BASIC. Upgrade your plan at https://rapidapi.com/DataCrawler/api/booking-com15'}"):
                logging.error("API subscription expired")

            id_data = 0
            try:
                while answer['data'][id_data]['search_type'] != 'city':
                    id_data += 1
                data['dest_id'] = answer['data'][id_data]['dest_id']
            except IndexError:
                bot.reply_to(message, 'Попробуйте еще раз ввести название города')

            bot.set_state(message.from_user.id, InfoHotel.min_cost, message.chat.id)
            bot.send_message(message.from_user.id, f"Введите минимальную стоимость отеля в долларах")
        else:
            bot.reply_to(message, 'Название города должно состоять из латинский символов, попробуйте еще раз')
    except Exception as err:
        logging.error(f"Error city{err}")


@bot.message_handler(state=InfoHotel.min_cost)
def get_min_cost(message: Message) -> None:
    try:
        try:
            if int(message.text) > 0:
                with bot.retrieve_data(message.chat.id) as data:
                    data['min_p'] = int(message.text)
                bot.set_state(message.from_user.id, InfoHotel.max_cost, message.chat.id)
                bot.send_message(message.from_user.id, f"Введите максимальную стоимость отеля в долларах")
            else:
                bot.send_message(message.from_user.id, f"Число должно быть положительным, попробуйте еще раз")
        except ValueError:
            bot.send_message(message.from_user.id, f"Необходимо ввести число, попробуйте еще раз")
    except Exception as err:
        logging.error(f"Error min cost {err}")


@bot.message_handler(state=InfoHotel.max_cost)
def get_max_cost(message: Message) -> None:
    try:
        calendar, step = DetailedTelegramCalendar().build()
        try:
            if int(message.text) > 0:
                with bot.retrieve_data(message.chat.id) as data:
                    data['max_p'] = int(message.text)
                if data['max_p'] < data['min_p']:
                    bot.send_message(message.from_user.id,
                                     "Максимальная сумма не может быть меньше минимальной, давай еще раз")
                else:
                    bot.send_message(message.from_user.id,
                                     "Введите дату заезда")
                    bot.set_state(message.from_user.id, InfoHotel.checkInDate, message.chat.id)
                    bot.send_message(message.from_user.id,
                                     f"Select {LSTEP[step]}",
                                     reply_markup=calendar)
            else:
                bot.send_message(message.from_user.id, f"Число должно быть положительным, попробуйте еще раз")
        except ValueError:
            bot.send_message(message.from_user.id, f"Необходимо ввести число, попробуйте еще раз")
    except Exception as err:
        logging.error(f"Error max cost {err}")


@bot.message_handler(state=InfoHotel.checkInDate)
def get_checkInDate(message: Message) -> None:
    try:
        bot.set_state(message.from_user.id, InfoHotel.checkOutDate, message.chat.id)
        bot.send_message(message.from_user.id,
                         "Введите дату выезда")
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.from_user.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
    except Exception as err:
        logging.error(f"Error first date {err}")


@bot.message_handler(state=InfoHotel.adults)
def get_adults(message: Message) -> None:
    try:
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.chat.id) as data:
                data['adults'] = int(message.text)
                data['children'] = list()
            bot.set_state(message.from_user.id, InfoHotel.children, message.chat.id)
            markup = an_children.ans_children()
            bot.send_message(message.from_user.id,
                             'Отлично. Будут ли дети?', reply_markup=markup)
        else:
            bot.send_message(message.from_user.id,
                             'Число должно быть не меньше 1 и не больше 10, попробуйте еще раз')
    except Exception as err:
        bot.send_message(message.chat.id, 'Необходимо ввести число, попробуйте еще раз')
        logging.error(f'Error second date {err}')


@bot.message_handler(state=InfoHotel.children)
def get_children_count(message: Message) -> None:
    try:
        try:
            if 1 <= int(message.text) <= 10:
                with bot.retrieve_data(message.chat.id) as data:
                    data['children_count'] = int(message.text)
                    data['children'] = list()
                if data['children_count'] == 0:
                    markup = need_photo.need_photo()
                    bot.set_state(message.chat.id, InfoHotel.need_photo)
                    bot.send_message(message.chat.id, f"Нужны ли вам фотографии отелей?", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, 'Напишите возраст первого ребенка')
                    bot.set_state(message.from_user.id, InfoHotel.get_children, message.chat.id)
            else:
                bot.send_message(message.from_user.id,
                                 'Число должно быть не меньше 1 и не больше 10, попробуйте еще раз')
        except ValueError:
            bot.send_message(message.chat.id, 'Необходимо ввести число, попробуйте еще раз')
    except Exception as err:
        logging.error(f"Error children {err}")


@bot.message_handler(state=InfoHotel.get_children)
def get_children(message: Message) -> None:
    with bot.retrieve_data(message.chat.id) as data:
        if data['children_count'] == 0:
            present(message)
    try:
        if 0 <= int(message.text) <= 18:
            with bot.retrieve_data(message.chat.id) as data:
                pass
            if data['children_count'] > 1:
                bot.send_message(message.chat.id, 'Напишите возраст следующего ребенка')
            if data['children_count'] != 0:
                with bot.retrieve_data(message.chat.id) as data:
                    data['children'].append(int(message.text))
                    data['children_count'] -= 1
            if data['children_count'] == 0:
                markup = need_photo.need_photo()
                bot.set_state(message.chat.id, InfoHotel.need_photo)
                bot.send_message(message.chat.id, f"Нужны ли вам фотографии отелей?", reply_markup=markup)
            else:
                pass
        else:
            bot.send_message(message.chat.id, 'Число не может быть отрицательным или больше 18, попробуйте еще раз')

    except ValueError:
        bot.send_message(message.chat.id, 'Необходимо написать число, попробуйте еще раз')


@bot.message_handler(state=InfoHotel.count)
def get_count(message: Message) -> None:
    try:
        if 1 <= int(message.text) <= 25:
            with bot.retrieve_data(message.chat.id) as data:
                data['count'] = int(message.text)
            present(message)
        else:
            bot.send_message(message.from_user.id,
                             'Число должно быть не меньше 1 и не больше 25, попробуйте еще раз')
    except ValueError:
        bot.send_message(message.chat.id, 'Необходимо ввести число, попробуйте еще раз')


def present(message: Message) -> None:
    # try:
    CRUD.create_table()
    CRUD.add_new_user(f"{message.from_user.first_name} {message.from_user.last_name}", message.from_user.id)
    with bot.retrieve_data(message.chat.id) as data:
        numb = CRUD.add_new_city(message.from_user.id, data['City'])

    bot.set_state(message.from_user.id, None, message.chat.id)
    bot.send_message(message.from_user.id, 'Отлично. Сейчас появится список отелей')

    dict_for_list = dict()
    with bot.retrieve_data(message.chat.id) as data:
        dict_for_list["dest_id"] = data["dest_id"]
        dict_for_list["fmonth"] = data["fmonth"]
        dict_for_list["fday"] = data["fday"]
        dict_for_list["fyear"] = data["fyear"]
        dict_for_list["sday"] = data["sday"]
        dict_for_list["smonth"] = data["smonth"]
        dict_for_list["syear"] = data["syear"]
        dict_for_list["adults"] = data["adults"]
        dict_for_list["children"] = data["children"]
        dict_for_list["max_p"] = data["max_p"]
        dict_for_list["min_p"] = data["min_p"]
        dict_for_list["sort"] = data["sort"]
        data["list"] = api.properties_list(dict_for_list)

        if not data["list"]["status"]:
            print('1')
            bot.send_message(message.from_user.id, data["list"]["message"]["message"])
            return
        pr_dict = data["list"]["data"]["hotels"]
        if data['command'] == '/highprice':
            pr_dict = list(reversed(data["list"]["data"]["hotels"]))
    count_hotel = 0

    print(pr_dict)
    for key in pr_dict:
        if count_hotel == data["count"]:
            break
        count_hotel += 1
        nd_photo = 0
        dict_for_detail = dict()
        dict_for_detail['propertyId'] = key["hotel_id"]
        dict_for_detail['fday'] = data["fday"]
        dict_for_detail['fmonth'] = data["fmonth"]
        dict_for_detail['fyear'] = data["fyear"]
        dict_for_detail['sday'] = data["sday"]
        dict_for_detail['smonth'] = data["smonth"]
        dict_for_detail['syear'] = data["syear"]
        dict_for_detail['adults'] = data["adults"]
        dict_for_detail['children'] = data["children"]
        with bot.retrieve_data(message.chat.id) as data:
            if data['need_photo'] == 1:
                nd_photo = 1
            hotel = api.properties_detail(dict_for_detail)

        info_hotel = hotel["data"]
        try:
            text = (
                f"Название: {info_hotel['hotel_name']}\nАдрес: {info_hotel['address']}\n"
                f"Стоимость проживания: {round(key['property']['priceBreakdown']['grossPrice']['value'], 3)}$\n"
                f"Рейтинг: {key['property']['propertyClass']}⭐️\n"
                f"Оценка посетителей: {key['property']['reviewScore']}\n"
                # f"Расстояние от центра: {key['destinationInfo']['distanceFromDestination']['value']} миль")
            )
        except TypeError:
            text = (
                f"Название: {info_hotel['hotel_name']}\nАдрес: {info_hotel['address']}\n"
                f"Стоимость проживания: {round(key['property']['priceBreakdown']['grossPrice']['value'], 3)}$\n"
                f"Оценка посетителей: {key['property']['reviewScore']}\n"
                # f"Расстояние от центра: {key['destinationInfo']['distanceFromDestination']['value']} миль"
            )

        photos = list()
        if nd_photo == 1:
            f = urllib.request.urlopen(info_hotel['url']).read()

            f = f.decode()
            need = r'data-thumb-url=".{145}'

            full_search = re.findall(need, f)

            stop_photo = 0
            for photo in full_search:
                stop_photo += 1
                photos.append(photo[16:145])
                if stop_photo == 3:
                    break

        media = list()
        if len(photos) > 0:
            for num, url in enumerate(photos):
                if num == 0:
                    media.append(InputMediaPhoto(media=url, caption=text))
                else:
                    media.append(InputMediaPhoto(media=url))
            bot.send_media_group(message.from_user.id, media)
        else:
            bot.send_message(message.from_user.id, text)

        photos_for_history = ' '.join(photos)
        CRUD.add_new_hotel(info_hotel['hotel_name'], info_hotel['address'],
                           round(key['property']['priceBreakdown']['grossPrice']['value'], 3),
                           key['property']['propertyClass'],
                           key['property']['reviewScore'], numb,
                           message.from_user.id, photos_for_history)

    if count_hotel != 0:
        bot.send_message(message.from_user.id, 'Вот все отели, что я смог найти')
    else:
        bot.send_message(message.from_user.id, 'Мне не удалось найти отели, соответствующие вашим критериям')
# except Exception as err:
#     bot.send_message(message.from_user.id, 'Произошла какая-то ошибка, попробуйте еще раз')
#     logging.error(f"Error present{err}")
