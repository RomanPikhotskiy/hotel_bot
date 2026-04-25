from api import api


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


def test_locations_search_returns_json_and_sends_city(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, params=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["params"] = params
        return _Response({"data": [{"dest_id": "1"}]})

    monkeypatch.setattr(api.requests, "get", fake_get)

    result = api.locations_search("Moscow")

    assert result == {"data": [{"dest_id": "1"}]}
    assert captured["url"].endswith("searchDestination")
    assert captured["params"] == {"query": "Moscow"}
    assert captured["headers"]["x-rapidapi-host"] == "booking-com15.p.rapidapi.com"


def test_properties_list_builds_query_with_children_and_zero_padding(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, params=None):
        captured["url"] = url
        captured["params"] = params
        return _Response({"status": True})

    monkeypatch.setattr(api.requests, "get", fake_get)

    data = {
        "dest_id": "city-1",
        "fyear": 2026,
        "fmonth": 1,
        "fday": 2,
        "syear": 2026,
        "smonth": 3,
        "sday": 4,
        "adults": 2,
        "children": [6, 10],
        "min_p": 10,
        "max_p": 200,
        "sort": "price",
    }

    result = api.properties_list(data)

    assert result == {"status": True}
    assert captured["url"].endswith("searchHotels")
    assert captured["params"]["arrival_date"] == "2026-01-02"
    assert captured["params"]["departure_date"] == "2026-03-04"
    assert captured["params"]["children_age"] == "6,10"
    assert captured["params"]["price_min"] == "10"
    assert captured["params"]["price_max"] == "200"


def test_properties_detail_builds_query_without_children(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, params=None):
        captured["url"] = url
        captured["params"] = params
        return _Response({"data": {"hotel_name": "Hotel"}})

    monkeypatch.setattr(api.requests, "get", fake_get)

    data = {
        "propertyId": "hotel-1",
        "fyear": 2026,
        "fmonth": 12,
        "fday": 31,
        "syear": 2027,
        "smonth": 1,
        "sday": 5,
        "adults": 1,
        "children": [],
    }

    result = api.properties_detail(data)

    assert result == {"data": {"hotel_name": "Hotel"}}
    assert captured["url"].endswith("getHotelDetails")
    assert captured["params"]["arrival_date"] == "2026-12-31"
    assert captured["params"]["departure_date"] == "2027-01-05"
    assert "children_age" not in captured["params"]
