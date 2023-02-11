import datetime

from django.shortcuts import render

from timeshift import timeshift_lib
from timeshift.models import City


# import logging
#
# logger = logging.getLogger('django.db.backends')
# logger.setLevel('DEBUG')
# logger.addHandler(logging.StreamHandler())


def index(request):
    response_data = dict()

    if request.method == 'POST':
        city_name = request.POST['city_name'].capitalize()
        abstract_api = timeshift_lib.Abstractapi()
        city_data = abstract_api.find_city(city_name)

        if not city_data.get('error'):
            city_data['local_time'] = abstract_api.get_local_time(
                city_data['gmt_offset']
            )

        try:
            city = City.objects.get(
                name=city_name,
            )
        except Exception:
            city = City.objects.create(
                name=city_name,
                gmt_offset=city_data['gmt_offset'],
                created_time=city_data['datetime']
            )

        response_data.update(city_data)

    return render(request, 'timeshift/index.html', response_data)


def get_cities(request):
    cities = City.objects.all()
    cities_list = []

    for city in cities:
        formatted_city = {
            'name': city.name,
            'time': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=city.gmt_offset)
        }
        cities_list.append(formatted_city)

    return render(request, 'timeshift/cities.html', {'cities': cities_list})
