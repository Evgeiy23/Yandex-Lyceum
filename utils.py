import requests


def get_map_image(lon, lat, zoom):
    map_url = "https://static-maps.yandex.ru/1.x/"
    params = {
        "ll": f"{lon},{lat}",
        "z": str(zoom),
        "l": "map",
        "size": "600,450"
    }
    response = requests.get(map_url, params=params)
    if response.status_code == 200:
        return response.content
    return None