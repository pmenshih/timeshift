from typing import Optional

import requests


class AbstractAPI:
    """Класс для обращения к API."""

    ABSTRACTAPI_URL = (
        'https://timezone.abstractapi.com/v1/current_time/?'
        'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
    )

    def __init__(self) -> None:
        self.cities = []

    def fetch_city_data(self, city_name: str) -> Optional[list[str, int]]:
        '''
        Достаем информацию о городе через API.
        '''
        city_data = requests.get(self.ABSTRACTAPI_URL + city_name).json()
        return [city_data['requested_location'], city_data['gmt_offset']]


class InMemoryAPIMock:
    ABSTRACTAPI_URL = (
        'https://timezone.abstractapi.com/v1/current_time/?'
        'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
    )

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
            city_data = requests.get(self.ABSTRACTAPI_URL + city_name).json()

            location = city_data['requested_location']
            print(f'Город {location} добавлен')

            return [city_data['requested_location'], city_data['gmt_offset']]
