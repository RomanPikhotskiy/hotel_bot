import datetime
from loader import bot
from database import db
from keyboards.inline import for_history


def create_table():
    db.Users.create_table()
    db.Cities.create_table()
    db.Hotels.create_table()


def add_new_user(name, id):
    if db.Users.select().where(db.Users.id_tg == id):
        pass
    else:
        new_user = db.Users(name=name, id_tg=id)
        new_user.save()


def add_new_city(id_user, city):
    n = db.Cities.select().where(db.Cities.user_id == id_user)
    numb = 0
    for x in n:
        numb = x.number + 1
    if len(n) == 10:
        numb -= 1
        db.Cities.delete().where(db.Cities.user_id == id_user, db.Cities.number == 0).execute()
        db.Hotels.delete().where(db.Hotels.user_id == id_user, db.Hotels.number == 0).execute()
        db.Cities.update(number=db.Cities.number - 1).where(db.Cities.user_id == id_user).execute()
        db.Hotels.update(number=db.Hotels.number - 1).where(db.Hotels.user_id == id_user).execute()

    new_city = db.Cities(number=numb, user_id=id_user, time=str(datetime.datetime.now()), name=city)
    new_city.save()
    return numb


def add_new_hotel(name, address, price, rating, preview, numb, id_user, photos):
    new_hotel = db.Hotels(name=name, address=address, price=price, rating=rating, preview=preview, number=numb,
                          user_id=id_user, photos=photos)
    new_hotel.save()


def draw_number(c) -> None:
    create_table()
    n = db.Cities.select().where(db.Cities.user_id == c.message.chat.id)

    numbers_h = dict()
    for x in n:
        numbers_h[x.number] = [x.time, x.name]
    if len(numbers_h) == 0:
        bot.send_message(c.message.chat.id, 'У вас еще нет истории поиска')
    else:

        markup = for_history.draw_num(numbers_h)

        for key in numbers_h:
            bot.send_message(c.message.chat.id,
                             f"({key + 1}) Дата и время: {numbers_h[key][0]}. Вы вводили {numbers_h[key][1]}")
            with bot.retrieve_data(c.message.chat.id) as data:
                data[
                    'history_present'] = f"({key + 1}) Дата и время: {numbers_h[key][0]}. Вы вводили {numbers_h[key][1]}"
        bot.send_message(c.message.chat.id, 'Выберите одну из историй', reply_markup=markup)
