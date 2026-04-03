import requests
from api import API_KEY


def geocode(address):
    url = "https://geocode-maps.yandex.ru/1.x"
    params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }

    r = requests.get(url, params=params)
    json_data = r.json()

    try:
        obj = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        pos = obj['Point']['pos']
        lon, lat = map(float, pos.split())
        return (lon, lat), obj['name']
    except (KeyError, IndexError, ValueError):
        return None, None


def get_map_image(lon, lat, zoom):
    map_url = "https://static-maps.yandex.ru/1.x/"
    params = {
        "ll": f"{lon},{lat}",
        "z": str(zoom),
        "l": "map"
    }
    response = requests.get(map_url, params=params)
    if response.status_code == 200:
        return response.content
    return None