from django.shortcuts import render

from timeshift import timeshift_lib as ts

def index(request):
    if request.method == 'POST':
        city_name = request.POST['city_name']
        api = ts.AbstractAPI()
        city_data = api.fetch_city_data(city_name)
        print('>>>', city_data)
    return render(request, 'timeshift/index.html')
