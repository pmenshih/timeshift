from django.shortcuts import render

from timeshift import timeshift_lib as ts

def index(request):
    response_data = dict()

    if request.method == 'POST':
        city_name = request.POST['city_name']
        api = ts.AbstractAPI()
        response_data = api.fetch_city_data(city_name)

        if not response_data.get('error', False):
            response_data['local_time'] = api.get_local_time(
                response_data['gmt_offset']
            )
        
    return render(request, 'timeshift/index.html', response_data)
