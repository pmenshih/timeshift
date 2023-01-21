'''
Программа вывода локального времени в городах.

Имеет меню с пунктами:
    1. Вывода списка имен городов и их локального времени.
    2. Добавление города.
    3. Выход из программы.

Поиск города осуществляется с помощью сервиса https://abstractapi.com.
В случае если полученное имя города найдено, его имя и часовой пояс
сохраняются в локальное хранилище программы.
'''
import datetime

import requests


def find_city():
    '''
    Поиск города с помощью https://abstractapi.com.

    Возвращает словарь с именем города и его часовым поясом.
    '''
    ABSTRACTAPI_URL = (
        'https://timezone.abstractapi.com/v1/current_time/?'
        'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
    )

    city_name = input('Введите название города: ')
    city_data = requests.get(ABSTRACTAPI_URL+city_name).json()

    if not city_data:
        print(f'Город с именем "{city_name}" найти не удалось.')
        return False
    
    return {
        'gmt_offset': city_data['gmt_offset'],
        'name': city_name
    }

def get_local_time(
    gmt_offset,
    base_time=datetime.datetime.now(datetime.timezone.utc)
):
    return (base_time + datetime.timedelta(hours=gmt_offset)).strftime('%H:%M')

def show_cities(cities):
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    for city_name in sorted(cities):
        local_time = get_local_time(cities[city_name], current_utc_time)

        print(f'{city_name}: {local_time}')

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
            show_cities(cities)
        # Поиск и добавление города.        
        elif command == '2':
            city_data = find_city()

            if not city_data:
                continue
            
            cities[city_data['name']] = city_data['gmt_offset']
            
            local_time = get_local_time(cities[city_data['name']])
            print(f'Текущее время в городе {city_data["name"]}: {local_time}')
        # Выход из программы.
        elif command == '3':
            break
        else:
            print(f'Неизвестная команда "{command}"')
