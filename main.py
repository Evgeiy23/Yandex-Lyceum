import sys
import requests
import math
from map_utils import get_spn_by_points
from api import API_KEY


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
        return (lon, lat), feature['name']
    except:
        return None, None


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    
    return math.sqrt(dx * dx + dy * dy)


def find_nearest_pharmacy(coords):
    lon, lat = coords
    
    search_url = "https://search-maps.yandex.ru/v1/"
    params = {
        'apikey': API_KEY,
        'text': 'аптека',
        'll': f'{lon},{lat}',
        'type': 'biz',
        'lang': 'ru_RU',
        'results': 5
    }
    
    response = requests.get(search_url, params=params)
    json_response = response.json()
    
    pharmacies = []
    for feature in json_response.get('features', []):
        pharmacy_coords = feature['geometry']['coordinates']
        pharmacy_lon, pharmacy_lat = pharmacy_coords
        
        distance = lonlat_distance(coords, (pharmacy_lon, pharmacy_lat))
        
        properties = feature['properties']
        name = properties.get('name', 'Неизвестно')
        address = properties.get('description', '')
        
        hours = properties.get('CompanyMetaData', {}).get('Hours', {})
        hours_text = hours.get('text', 'Режим работы не указан')
        
        pharmacies.append({
            'name': name,
            'address': address,
            'coords': (pharmacy_lon, pharmacy_lat),
            'distance': distance,
            'hours': hours_text
        })
    
    if not pharmacies:
        return None
    
    return min(pharmacies, key=lambda x: x['distance'])


def create_map(point1, point2, pharmacy):
    points = [point1, point2]
    center, spn = get_spn_by_points(points)
    
    pt1 = f"{point1[0]},{point1[1]},pm2gnm"
    pt2 = f"{point2[0]},{point2[1]},pm2rdm"
    
    map_url = "https://static-maps.yandex.ru/v1"
    map_params = {
        'apikey': API_KEY,
        'll': f"{center[0]},{center[1]}",
        'spn': f"{spn[0]},{spn[1]}",
        'pt': f"{pt1}~{pt2}",
        'size': '600,400',
        'lang': 'ru_RU'
    }
    
    response = requests.get(map_url, params=map_params)
    
    with open('pharmacy_map.png', 'wb') as f:
        f.write(response.content)
    
    print("Карта сохранена в pharmacy_map.png")


def main():
    if len(sys.argv) < 2:
        print("Укажите адрес в параметрах командной строки")
        return
    
    address = ' '.join(sys.argv[1:])
    
    coords, address_name = geocode(address)
    if not coords:
        print("Не удалось найти указанный адрес")
        return
    
    pharmacy = find_nearest_pharmacy(coords)
    if not pharmacy:
        print("Не найдено аптек рядом")
        return
    
    print("\n" + "="*50)
    print("БЛИЖАЙШАЯ АПТЕКА")
    print("="*50)
    print(f"Ваш адрес: {address_name}")
    print(f"Координаты: {coords[0]:.6f}, {coords[1]:.6f}")
    print("-"*50)
    print(f"Аптека: {pharmacy['name']}")
    print(f"Адрес: {pharmacy['address']}")
    print(f"Режим работы: {pharmacy['hours']}")
    print(f"Расстояние: {pharmacy['distance']:.0f} м")
    print("="*50)
    
    create_map(coords, pharmacy['coords'], pharmacy)


if __name__ == '__main__':
    main()