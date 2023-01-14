'''
Программа отображения локального времени в городах.
Содержит меню, состоящее из пунктов:
    1. Вывод списка городов и их локального времени
    2. Добавление нового города
    3. Выход из программы
Информация о часовом поясе города берется с сервиса abstractapi.com.
В случае нахождения города (его корректного имени) его имя и часовой пояс
сохраняется в локальный список программы.
'''
import datetime

import requests


ABSTRACTAPI_URL = (
    'https://timezone.abstractapi.com/v1/current_time/?'
    'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
)


def find_city():
    '''
    Поиск города и информации о его времени с помощью abstractapi.com.
    '''
    city_name = input('Введите имя города: ')

    city_data = requests.get(ABSTRACTAPI_URL + city_name).json()
    if not city_data:
        print(f'Город с именем "{city_name}" не найден.')
        return None

    print('Текущее время:', get_local_time(city_data['gmt_offset']))

    return {
        'gmt_offset': city_data['gmt_offset'],
        'name': city_name,
    }

def get_local_time(
    gmt_offset,
    current_utc_time=datetime.datetime.now(datetime.timezone.utc)
):
    '''
    Определение текущего времени по значению часового пояса.

    Параметры:
        - `gmt_offset`: смещение в часах относительно времени UTC;
        - `current_utc_time`: текущее время UTC.
    '''
    return (
        current_utc_time + datetime.timedelta(hours=gmt_offset)
    ).strftime('%H:%M')

def show_cities_list(cities):
    for city_name in sorted(cities):
        print(f'{city_name}: {get_local_time(cities[city_name])}')

def show_menu():
    print(
        '\nВведите команду:\n'
        '1. Вывести список городов\n'
        '2. Добавить город\n'
        '3. Выход'
    )


if __name__ == '__main__':
    cities = dict()

    while True:
        show_menu()

        command = input('>>> ')
        print()

        # Вывод списка городов.
        if command == '1':
            show_cities_list(cities)
        # Поиск и добавление нового города.
        elif command == '2':
            city_data = find_city()
            if not city_data:
                continue
            cities[city_data['name']] = city_data['gmt_offset']
        # Выход из программы.
        elif command == '3':
            break
        # Неизвестная команда.
        else:
            print(f'Неизвестная команда "{command}"')
