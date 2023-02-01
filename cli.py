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

from auxutils import get_local_time
from timeshiftlib import AbstractAPI, InMemoryAPIMock


# Протоколы позволяют определять интерфейс
# без прямой необходимости наследования.
# Если мы уберём наследование от протокола, то mypy будет ругаться,
# что класс AbstractAPI не может быть использован в классе Application

# Здесь мы определили интерфейс,которому должны следовать классы,
# которые хотят чтобы наше приложение ими воспользовалось.
class CityDataFetcher(Protocol):

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


class Application:
    '''
    Класс приложения.

    Содержит в себе логику обработки пользовательских команд.
    '''

    def __init__(self, fetcher):
        self.fetcher = fetcher

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
            for city_name in sorted(list(self.fetcher.cities.keys())):
                local_time = get_local_time(
                    self.fetcher.fetch_city_data(city_name),
                    current_utc_time)
                print(
                    f'{city_name}: {local_time}'
                )
        else:
            print('Вы используете AbstractAPI')

    def add_city(self):
        '''
        Метод получает информацию о городе, который интересует пользователя,
        используя реализацию `self.fetcher`, после чего выводит на экран
        текущее время в городе.
        '''
        city_name = input('Введите имя города: ')

        city_data = self.fetcher.fetch_city_data(city_name)

        if not city_data:
            print(f'Город с именем "{city_name}" не найден.')
            return

        print('Текущее время:', get_local_time(city_data['gmt_offset']))

        city = City(city_name, city_data['gmt_offset'])
        self.cities[city_name] = city

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
        fetcher = InMemoryAPIMock(
            {
                "Moscow": {'gmt_offset': 3},
                "Paris": {'gmt_offset': 1},
                "Berlin": {'gmt_offset': 1}
            }
        )
    else:
        # в противном случае используем настоящую реализацию.
        fetcher = AbstractAPI()

    app = Application(fetcher)
    while True:
        # Главный цикл нашего приложения.
        # Показываем меню и обрабатываем ввод пользователя.
        app.show_menu()
        app.handle_user_input()
