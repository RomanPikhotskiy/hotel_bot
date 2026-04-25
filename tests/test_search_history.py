from database import CRUD, db


def test_add_new_city_keeps_only_last_ten_records(isolated_db):
    CRUD.create_table()
    user_id = 501

    last_number = None
    for index in range(11):
        last_number = CRUD.add_new_city(user_id, f"City {index}")

    cities = list(
        db.Cities.select().where(db.Cities.user_id == user_id).order_by(db.Cities.number)
    )

    assert last_number == 9
    assert len(cities) == 10
    assert [city.number for city in cities] == list(range(10))
    assert cities[0].name == "City 1"
    assert cities[-1].name == "City 10"


def test_draw_number_sends_empty_history_message(monkeypatch, isolated_db, fake_bot, callback_factory):
    monkeypatch.setattr(CRUD, "bot", fake_bot)
    callback = callback_factory(chat_id=777)

    CRUD.draw_number(callback)

    assert len(fake_bot.messages) == 1
    assert fake_bot.messages[0]["reply_markup"] is None


def test_draw_number_sends_history_with_keyboard(monkeypatch, isolated_db, fake_bot, callback_factory):
    CRUD.create_table()
    user_id = 888
    CRUD.add_new_city(user_id, "Moscow")

    monkeypatch.setattr(CRUD, "create_table", lambda: None)
    monkeypatch.setattr(CRUD, "bot", fake_bot)
    monkeypatch.setattr(CRUD.for_history, "draw_num", lambda numbers: "history_markup")
    callback = callback_factory(chat_id=user_id)

    CRUD.draw_number(callback)

    assert len(fake_bot.messages) == 2
    assert fake_bot.messages[-1]["reply_markup"] == "history_markup"
    assert "history_present" in fake_bot.storage[user_id]
