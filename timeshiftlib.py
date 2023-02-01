from typing import Optional

import requests


class AbstractAPI:
    """Класс для обращения к API."""

    ABSTRACTAPI_URL = (
        'https://timezone.abstractapi.com/v1/current_time/?'
        'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
    )

    def fetch_city_data(self, city_name: str) -> Optional[dict[str, int]]:
        city_data = requests.get(self.ABSTRACTAPI_URL + city_name).json()
        return city_data


class InMemoryAPIMock:
    ABSTRACTAPI_URL = (
        'https://timezone.abstractapi.com/v1/current_time/?'
        'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
    )

    def __init__(self, cities: dict):
        self.cities = cities

    def fetch_city_data(self, city_name: str) -> Optional[dict[str, int]]:
        if city_name in list(self.cities.keys()):
            return self.cities.get(city_name)
        else:
            print(f'Город {city_name} не найден')
            city_data = requests.get(self.ABSTRACTAPI_URL + city_name).json()
            self.cities[city_data['requested_location']] = {'gmt_offset': city_data['gmt_offset']}
            location = city_data['requested_location']
            print(f'Город {location} добавлен')
