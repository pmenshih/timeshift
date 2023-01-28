from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        print('>>>> ', request.POST['city_name'])
    return render(request, 'timeshift/index.html')
