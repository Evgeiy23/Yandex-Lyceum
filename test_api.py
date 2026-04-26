from requests import get, post, delete

url = 'http://localhost:5000/api/v2/users'


def run_tests():
    print(" Список всех пользователей ")
    print(get(url).json())

    print("\n Добавление пользователя ")
    user_data = {
        'surname': 'Kharechkin',
        'name': 'Evgen',
        'age': 67,
        'position': 'programmer',
        'speciality': 'IT',
        'address': 'RTY_MIREA',
        'city_from': 'Moscow',
        'email': 'zharechkin.e@sch2009.net',
        'password': 'EGE100Ballov!'
    }
    print(post(url, json=user_data).json())

    print("\n Ошибка добавления (нет данных) ")
    print(post(url, json={'name': 'OnlyName'}).json())

    print("\n Получение пользователя по ID (1) ")
    print(get(f'{url}/1').json())

    print("\n Ошибка: пользователь не найден ")
    print(get(f'{url}/999').json())

    print("\n Удаление пользователя ")
    print(delete(f'{url}/2').json())

    print("\n Итоговый список ")
    print(get(url).json())


if __name__ == "__main__":
    run_tests()