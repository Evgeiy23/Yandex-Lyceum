from requests import get, post, delete

USER_URL = 'http://localhost:5000/api/v2/users'
JOB_URL = 'http://localhost:5000/api/v2/jobs'


def run_tests():
    print(" Ресурсы Пользователей ")
    print(get(USER_URL).json())
    print(post(USER_URL, json={
        'surname': 'Watney', 'name': 'Mark', 'age': 35,
        'position': 'botanist', 'speciality': 'researcher',
        'address': 'module_1', 'city_from': 'Chicago',
        'email': 'mark@mars.org', 'password': '123'
    }).json())
    print(get(f'{USER_URL}/1').json())
    print(delete(f'{USER_URL}/999').json())

    print("\n Ресурсы Работ ")
    print(get(JOB_URL).json())
    print(post(JOB_URL, json={
        'job': 'Solar Panel Repair', 'team_leader': 1,
        'work_size': 10, 'collaborators': '2, 3',
        'is_finished': False
    }).json())
    print(delete(f'{JOB_URL}/1').json())
    print(get(JOB_URL).json())


if __name__ == "__main__":
    run_tests()