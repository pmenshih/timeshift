from django.urls import path

from timeshift import views

app_name = 'timeshift'

urlpatterns = [
    path('', views.index, name='index')
]

