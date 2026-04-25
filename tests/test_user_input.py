from handlers.custom_handlers import lowprice


class _Calendar:
    def build(self):
        return "calendar_markup", 0


def test_get_min_cost_accepts_positive_number(monkeypatch, fake_bot, message_factory):
    monkeypatch.setattr(lowprice, "bot", fake_bot)
    message = message_factory("120")

    lowprice.get_min_cost(message)

    assert fake_bot.storage[message.chat.id]["min_p"] == 120
    assert fake_bot.states[-1] == (message.from_user.id, lowprice.InfoHotel.max_cost, message.chat.id)
    assert len(fake_bot.messages) == 1


def test_get_min_cost_rejects_non_number(monkeypatch, fake_bot, message_factory):
    monkeypatch.setattr(lowprice, "bot", fake_bot)
    message = message_factory("abc")

    lowprice.get_min_cost(message)

    assert len(fake_bot.messages) == 1
    assert "число" in fake_bot.messages[0]["text"].lower()


def test_get_max_cost_rejects_value_less_than_min(monkeypatch, fake_bot, message_factory):
    monkeypatch.setattr(lowprice, "bot", fake_bot)
    monkeypatch.setattr(lowprice, "DetailedTelegramCalendar", _Calendar)
    monkeypatch.setattr(lowprice, "LSTEP", {0: "day"})

    message = message_factory("50")
    fake_bot.storage[message.chat.id] = {"min_p": 100}

    lowprice.get_max_cost(message)

    assert fake_bot.storage[message.chat.id]["max_p"] == 50
    assert "меньше минимальной" in fake_bot.messages[-1]["text"].lower()


def test_get_adults_accepts_number_in_range(monkeypatch, fake_bot, message_factory):
    monkeypatch.setattr(lowprice, "bot", fake_bot)
    monkeypatch.setattr(lowprice.an_children, "ans_children", lambda: "children_markup")
    message = message_factory("3")

    lowprice.get_adults(message)

    assert fake_bot.storage[message.chat.id]["adults"] == 3
    assert fake_bot.storage[message.chat.id]["children"] == []
    assert fake_bot.states[-1] == (message.from_user.id, lowprice.InfoHotel.children, message.chat.id)
    assert fake_bot.messages[-1]["reply_markup"] == "children_markup"


def test_get_count_rejects_value_over_limit(monkeypatch, fake_bot, message_factory):
    monkeypatch.setattr(lowprice, "bot", fake_bot)
    message = message_factory("30")

    lowprice.get_count(message)

    assert len(fake_bot.messages) == 1
    assert "не больше 25" in fake_bot.messages[0]["text"].lower()
