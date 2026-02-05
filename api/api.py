import requests
from config_data import config

api_key = config.RAPID_API_KEY

headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "booking-com15.p.rapidapi.com"
}


def locations_search(city: str) -> dict:
    """
    Функция, которая делает запрос по api и возвращает json, по которому
    мы найдем id города
    """
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"

    querystring = {"query": city}

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def properties_list(dict_for_list: dict) -> dict:
    """
    Функция возвращает json со списком отелей подходящих под условия
    """

    children_list = ''
    for i in dict_for_list["children"]:

        if children_list == '':
            children_list += f"{i}"
        else:
            children_list += ',' + f'{i}'
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"

    sdate = f"{dict_for_list['syear']}-{dict_for_list['smonth']}-{dict_for_list['sday']}"
    fdate = f"{dict_for_list['fyear']}-{dict_for_list['fmonth']}-{dict_for_list['fday']}"
    if dict_for_list['fmonth'] < 10:
        fdate = f"{dict_for_list['fyear']}-0{dict_for_list['fmonth']}-{dict_for_list['fday']}"
    if dict_for_list['fday'] < 10:
        fdate = f"{dict_for_list['fyear']}-{dict_for_list['fmonth']}-0{dict_for_list['fday']}"
    if dict_for_list['fday'] < 10 and dict_for_list['fmonth'] < 10:
        fdate = f"{dict_for_list['fyear']}-0{dict_for_list['fmonth']}-0{dict_for_list['fday']}"
    if dict_for_list['smonth'] < 10:
        sdate = f"{dict_for_list['syear']}-0{dict_for_list['smonth']}-{dict_for_list['sday']}"
    if dict_for_list['sday'] < 10:
        sdate = f"{dict_for_list['syear']}-{dict_for_list['smonth']}-0{dict_for_list['sday']}"
    if dict_for_list['sday'] < 10 and dict_for_list['smonth'] < 10:
        sdate = f"{dict_for_list['syear']}-0{dict_for_list['smonth']}-0{dict_for_list['sday']}"

    if children_list == '':
        querystring = {"dest_id": dict_for_list['dest_id'],
                       "search_type": "CITY",
                       "arrival_date": fdate,
                       "departure_date": sdate,
                       "adults": f"{dict_for_list['adults']}",
                       "price_min": f"{dict_for_list['min_p']}",
                       "price_max": f"{dict_for_list['max_p']}",
                       "sort_by": f"{dict_for_list['sort']}"

                       }
    else:
        querystring = {"dest_id": dict_for_list['dest_id'],
                       "search_type": "CITY",
                       "arrival_date": fdate,
                       "departure_date": sdate,
                       "adults": f"{dict_for_list['adults']}",
                       "children_age": children_list,
                       "price_min": f"{dict_for_list['min_p']}",
                       "price_max": f"{dict_for_list['max_p']}",
                       "sort_by": f"{dict_for_list['sort']}"

                       }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def properties_detail(dict_for_list: dict) -> dict:
    """
    Функция, которая возвращает json с полной информацией по конкретному отелю
    """
    children_list = ''
    for i in dict_for_list['children']:
        if children_list == '':
            children_list += f"{i}"
        else:
            children_list += ',' + f'{i}'
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelDetails"

    sdate = f"{dict_for_list['syear']}-{dict_for_list['smonth']}-{dict_for_list['sday']}"
    fdate = f"{dict_for_list['fyear']}-{dict_for_list['fmonth']}-{dict_for_list['fday']}"
    if dict_for_list['fmonth'] < 10:
        fdate = f"{dict_for_list['fyear']}-0{dict_for_list['fmonth']}-{dict_for_list['fday']}"
    if dict_for_list['fday'] < 10:
        fdate = f"{dict_for_list['fyear']}-{dict_for_list['fmonth']}-0{dict_for_list['fday']}"
    if dict_for_list['fday'] < 10 and dict_for_list['fmonth'] < 10:
        fdate = f"{dict_for_list['fyear']}-0{dict_for_list['fmonth']}-0{dict_for_list['fday']}"
    if dict_for_list['smonth'] < 10:
        sdate = f"{dict_for_list['syear']}-0{dict_for_list['smonth']}-{dict_for_list['sday']}"
    if dict_for_list['sday'] < 10:
        sdate = f"{dict_for_list['syear']}-{dict_for_list['smonth']}-0{dict_for_list['sday']}"
    if dict_for_list['sday'] < 10 and dict_for_list['smonth'] < 10:
        sdate = f"{dict_for_list['syear']}-0{dict_for_list['smonth']}-0{dict_for_list['sday']}"

    print(dict_for_list['propertyId'])
    if children_list == '':
        querystring = {"hotel_id": dict_for_list['propertyId'],
                       "arrival_date": fdate,
                       "departure_date": sdate,
                       "adults": f"{dict_for_list['adults']}",

                       }
    else:
        querystring = {"hotel_id": dict_for_list['propertyId'],
                       "arrival_date": fdate,
                       "departure_date": sdate,
                       "adults": f"{dict_for_list['adults']}",
                       "children_age": children_list,

                       }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
