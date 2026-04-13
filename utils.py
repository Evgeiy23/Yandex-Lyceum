import requests
import math
from api import API_KEY, SEARCH_API_KEY


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def geocode(query):
    url = "https://geocode-maps.yandex.ru/1.x"
    params = {
        'apikey': API_KEY,
        'geocode': query,
        'format': 'json'
    }
    try:
        r = requests.get(url, params=params)
        json_data = r.json()
        geo_obj = json_data['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']
        pos = geo_obj['Point']['pos']
        meta_data = geo_obj['metaDataProperty']['GeocoderMetaData']
        address_str = meta_data['text']
        address_details = meta_data.get('Address', {})
        postal_code = address_details.get('postal_code', "")
        return tuple(map(float, pos.split())), address_str, postal_code
    except Exception:
        return None, None, None


def find_business(ll):
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": SEARCH_API_KEY,
        "text": "организация",
        "ll": f"{ll[0]},{ll[1]}",
        "type": "biz",
        "lang": "ru_RU",
        "results": 1
    }
    try:
        r = requests.get(url, params=params)
        json_data = r.json()
        if not json_data.get("features"):
            return None, None, None
        
        feature = json_data["features"][0]
        pos = feature["geometry"]["coordinates"]
        
        if lonlat_distance(ll, pos) > 50:
            return None, None, None
            
        prop = feature["properties"]
        name = prop.get("name")
        address = prop["CompanyMetaData"].get("address", "")
        
        return tuple(pos), f"{name}, {address}", ""
    except Exception:
        return None, None, None


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