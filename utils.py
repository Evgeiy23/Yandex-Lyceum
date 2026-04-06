import requests
from api import API_KEY


def geocode(address):
    url = "https://geocode-maps.yandex.ru/1.x"
    params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    try:
        r = requests.get(url, params=params)
        json_data = r.json()
        pos = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return tuple(map(float, pos.split()))
    except Exception:
        return None


def get_map_image(lon, lat, zoom, theme="light", marker=None):
    map_url = "https://static-maps.yandex.ru/1.x/"
    params = {
        "ll": f"{lon},{lat}",
        "z": str(zoom),
        "l": "map",
        "theme": theme,
        "size": "600,450"
    }
    if marker:
        params["pt"] = f"{marker[0]},{marker[1]},pm2rdm"

    response = requests.get(map_url, params=params)
    if response.status_code == 200:
        return response.content
    return None