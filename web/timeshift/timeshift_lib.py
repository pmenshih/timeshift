import datetime

import requests


ABSTRACTAPI_URL = (
    'https://timezone.abstractapi.com/v1/current_time/?'
    'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
)

class AbstractAPI:
    """Класс для обращения к API."""

    def __init__(self) -> None:
        self.cities = []

    def fetch_city_data(self, city_name: str) -> dict:
        '''
        Достаем информацию о городе через API.
        '''
        city_data = requests.get(ABSTRACTAPI_URL + city_name).json()
        
        if not city_data or city_data.get('error', False):
            return {
                'error': f'Город с именем {city_name} не найден.'
            }

        return {
            'gmt_offset': city_data['gmt_offset'],
            'name': city_name,
        }
    
    def get_local_time(
        self,
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


class InMemoryAPIMock:
    def __init__(self, cities: list):
        self.cities = cities

    def fetch_city_data(self, city_name):
        '''
        Доставем информацию о городе из БД и если не получается
        заправшиваем ее через API
        '''
        if city_name in self.cities:
            return city_name.timezone
        else:
            print(f'Город {city_name} не найден')
            city_data = requests.get(ABSTRACTAPI_URL + city_name).json()

            location = city_data['requested_location']
            print(f'Город {location} добавлен')

            return {
                'gmt_offset': city_data['gmt_offset'],
                'name': city_name,
            }
