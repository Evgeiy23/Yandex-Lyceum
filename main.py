import sys
import requests
from map_utils import get_spn_by_points
from api import API_KEY


def geocode(address):
    url = "https://geocode-maps.yandex.ru/1.x"
    params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    
    r = requests.get(url, params=params)
    json = r.json()
    
    try:
        obj = json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        pos = obj['Point']['pos']
        lon, lat = map(float, pos.split())
        return (lon, lat), obj['name']
    except:
        return None, None


def is_24_7(hours):
    if not hours:
        return False
    h = hours.lower()
    return 'круглосуточно' in h or '24' in h


def get_color(pharmacy):
    if pharmacy['hours'] and is_24_7(pharmacy['hours']):
        return 'gn'
    elif pharmacy['hours']:
        return 'bl'
    else:
        return 'gr'


def find_pharmacies(coords):
    lon, lat = coords
    
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        'apikey': API_KEY,
        'text': 'аптека',
        'll': f'{lon},{lat}',
        'type': 'biz',
        'lang': 'ru_RU',
        'results': 10
    }
    
    r = requests.get(url, params=params)
    json = r.json()
    
    pharmacies = []
    for f in json.get('features', []):
        coords = f['geometry']['coordinates']
        props = f['properties']
        name = props.get('name', 'Неизвестно')
        addr = props.get('description', '')
        
        meta = props.get('CompanyMetaData', {})
        hours = meta.get('Hours', {}).get('text', '')
        
        pharmacies.append({
            'name': name,
            'address': addr,
            'coords': (coords[0], coords[1]),
            'hours': hours
        })
    
    return pharmacies


def make_map(addr_coords, pharmacies):
    points = [addr_coords] + [p['coords'] for p in pharmacies]
    center, spn = get_spn_by_points(points)
    
    pts = [f"{addr_coords[0]},{addr_coords[1]},pm2gnm"]
    
    for p in pharmacies:
        color = get_color(p)
        pts.append(f"{p['coords'][0]},{p['coords'][1]},pm2{color}m")
    
    url = "https://static-maps.yandex.ru/v1"
    params = {
        'apikey': API_KEY,
        'll': f"{center[0]},{center[1]}",
        'spn': f"{spn[0]},{spn[1]}",
        'pt': '~'.join(pts),
        'size': '600,400',
        'lang': 'ru_RU'
    }
    
    r = requests.get(url, params=params)
    
    with open('map.png', 'wb') as f:
        f.write(r.content)
    
    print("Карта в map.png")


def main():
    if len(sys.argv) < 2:
        print("Напиши адрес в параметрах")
        return
    
    addr = ' '.join(sys.argv[1:])
    
    coords, name = geocode(addr)
    if not coords:
        print("Адрес не найден")
        return
    
    pharmacies = find_pharmacies(coords)
    if not pharmacies:
        print("Аптек нет")
        return
    
    print(f"\nАдрес: {name}")
    print(f"Нашел {len(pharmacies)} аптек:\n")
    
    for i, p in enumerate(pharmacies, 1):
        hours = p['hours'] if p['hours'] else "нет данных"
        if len(hours) > 20:
            hours = hours[:17] + "..."
        print(f"{i}. {p['name'][:25]} - {hours}")
    
    print("\nЦвета:")
    print("зеленый - круглосуточно")
    print("синий - есть режим")
    print("серый - нет данных")
    
    make_map(coords, pharmacies)


if __name__ == '__main__':
    main()