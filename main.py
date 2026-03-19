import requests
from map_utils import get_spn

API_KEY = 'API_KEY from the textbook'


def geocode(address):
    url = "https://geocode-maps.yandex.ru/1.x"
    params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    json_response = response.json()
    
    try:
        feature = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        pos = feature['Point']['pos']
        lon, lat = map(float, pos.split())
        
        envelope = feature['boundedBy']['Envelope']
        lower_corner = envelope['lowerCorner'].split()
        upper_corner = envelope['upperCorner'].split()
        
        lower_lon, lower_lat = float(lower_corner[0]), float(lower_corner[1])
        upper_lon, upper_lat = float(upper_corner[0]), float(upper_corner[1])
        
        return (lon, lat), (lower_lon, lower_lat, upper_lon, upper_lat), feature['name']
    except:
        return None, None, None


def show_map(address):
    result = geocode(address)
    
    if not result[0]:
        print("Объект не найден")
        return
    
    coords, bounds, name = result
    lon, lat = coords
    lower_lon, lower_lat, upper_lon, upper_lat = bounds
    
    spn_lon, spn_lat = get_spn(lower_lon, lower_lat, upper_lon, upper_lat)
    
    map_url = "https://static-maps.yandex.ru/v1"
    map_params = {
        'apikey': API_KEY,
        'll': f"{lon},{lat}",
        'spn': f"{spn_lon},{spn_lat}",
        'pt': f"{lon},{lat},pm2rdm",
        'size': '600,400',
        'lang': 'ru_RU'
    }
    
    response = requests.get(map_url, params=map_params)
    
    with open('map.png', 'wb') as f:
        f.write(response.content)
    
    print(f"Найден объект: {name}")
    print(f"Координаты: {lon:.6f}, {lat:.6f}")
    print(f"Масштаб: {spn_lon:.6f}° x {spn_lat:.6f}°")
    print("Карта сохранена в map.png")


def main():
    address = input("Введите адрес: ")
    show_map(address)


if __name__ == '__main__':
    main()