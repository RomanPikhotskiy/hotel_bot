from peewee import *

dbs = SqliteDatabase('history.db')


class Users(Model):
    name = CharField()
    id_tg = DateField()

    class Meta:
        database = dbs


class Cities(Model):
    name = CharField()
    user_id = DateField()
    number = DateField()
    time = CharField()

    class Meta:
        database = dbs


class Hotels(Model):
    name = CharField()
    address = CharField()
    price = DecimalField()
    rating = CharField()
    preview = CharField()
    user_id = IntegerField()
    number = IntegerField()
    photos = CharField()

    class Meta:
        database = dbs
