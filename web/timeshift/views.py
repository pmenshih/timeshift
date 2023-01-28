from django.shortcuts import render

from timeshift import timeshift_lib

def index(request):
    response_data = dict()

    if request.method == 'POST':
        city_name = request.POST['city_name']
        abstract_api = timeshift_lib.Abstractapi()
        city_data = abstract_api.find_city(city_name)

        if not city_data.get('error'):
            city_data['local_time'] = abstract_api.get_local_time(
                city_data['gmt_offset']
            )

        response_data.update(city_data)

    return render(request, 'timeshift/index.html', response_data)
