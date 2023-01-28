import requests
import datetime


class Provider:

    def show_cities_list(self, cities):
        for city_name in sorted(cities):
            print(f'{city_name}: {self.get_local_time(cities[city_name])}')

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


class Abstractapi(Provider):
    ABSTRACTAPI_URL = (
        'https://timezone.abstractapi.com/v1/current_time/?'
        'api_key=30a9c393ff8c4585bec59a8a02cfe5be&location='
    )

    def find_city(self, city_name):
        '''
        Поиск города и информации о его времени с помощью abstractapi.com.
        '''

        city_data = requests.get(self.ABSTRACTAPI_URL + city_name).json()
        if not city_data:
            # print(f'Город с именем "{city_name}" не найден.')
            return None

        # print('Текущее время:', self.get_local_time(city_data['gmt_offset']))

        return {
            'gmt_offset': city_data['gmt_offset'],
            'name': city_name,
        }

