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
import sys

from typing import Optional, Protocol

import timeshift_lib as tsl
from timeshift_lib import AbstractAPI, InMemoryAPIMock


# Протоколы позволяют определять интерфейс
# без прямой необходимости наследования.
# Если мы уберём наследование от протокола, то mypy будет ругаться,
# что класс AbstractAPI не может быть использован в классе Application

class CityDataFetcher(Protocol):
    '''
    Здесь мы определили интерфейс,которому должны следовать классы,
    которые хотят чтобы наше приложение ими воспользовалось.
    '''

    # Функция должна вернуть словарь с ключом gmt_offset
    def fetch_city_data(self, city_name: str) -> Optional[dict[str, int]]:
        '''
        Метод принимает имя города `city_name` и возвращает словарь,
        где под ключём `gmt_offset` должен лежать сдвиг таймзоны
       в которой находится город `city_name` относительно GMT
        '''
        ...


class City:
    '''
    Класс города.
    '''
    def __init__(self, name: str, timezone: int):
        self.name = name
        self.timezone = timezone

    def __str__(self) -> str:
        return f'{self.name}'


class Application:
    '''
    Класс приложения.

    Содержит в себе логику обработки пользовательских команд.
    '''

    def __init__(self, fetcher):
        self.fetcher = fetcher

        # self.cities = dict()
        self.commands = {
            '1': self.show_cities_list,
            '2': self.add_city,
            '3': self.exit,
        }

    def show_menu(self):
        print(
            '\nВведите команду:\n'
            '1. Вывести список городов\n'
            '2. Добавить город\n'
            '3. Выход'
        )

    def handle_user_input(self):
        command = input('>>> ')
        if command not in self.commands:
            print(f'Неизвестная команда "{command}"')
            return
        self.commands[command]()

    def show_cities_list(self):
        '''
        Метод выводит список городов на экран.
        '''
        current_utc_time = datetime.datetime.now(datetime.timezone.utc)
        if self.fetcher.__class__.__name__ == 'InMemoryAPIMock':
            # проверяем через какой обьект мы работаем
            # если через БД, то выводим данные котоыре находятся в БД
            for city_name in self.fetcher.cities:
                local_time = self.fetcher.get_local_time(
                    self.fetcher.fetch_city_data(city_name),
                    current_utc_time)
                print(
                    f'{city_name}: {local_time}'
                )
        # если работаем через AbstractAPI то достаем из локального массива
        else:
            for city_name in self.fetcher.cities:
                local_time = self.fetcher.get_local_time(city_name.timezone)
                print(
                    f'{city_name}: {local_time}'
                )

    def add_city(self):
        '''
        Метод получает информацию о городе, который интересует пользователя,
        используя реализацию `self.fetcher`, после чего выводит на экран
        текущее время в городе.
        И добавляет его в базу данных,
        чтобы можно вывести вместе с общим списком
        '''
        city_name = input('Введите имя города: ')
        city_data = self.fetcher.fetch_city_data(city_name)

        if not city_data:
            return

        print('Текущее время:', self.fetcher.get_local_time(city_data[1]))
        # добавляем в БД
        new_city = City(city_name, city_data[1])
        self.fetcher.cities.append(new_city)

    def exit(self):
        '''
        Метод останавливает выполнение программы.
        '''
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Если программа была запущена как: python cli.py test
        # То используем реализацию фетчера данных
        # не использующую сторонний сервис, а хранящуюданные локально.
        Moscow = City('Moscow', 3)
        Paris = City('Paris', 1)
        Berlin = City('Berlin', 1)
        cities_list: list = [Moscow, Paris, Berlin]
        fetcher = InMemoryAPIMock(cities_list)
    else:
        # в противном случае используем настоящую реализацию.
        fetcher = AbstractAPI()

    app = Application(fetcher)
    while True:
        # Главный цикл нашего приложения.
        # Показываем меню и обрабатываем ввод пользователя.
        app.show_menu()
        app.handle_user_input()
