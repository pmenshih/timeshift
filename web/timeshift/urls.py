from django.urls import path

from timeshift import views

urlpatterns = [
    path('', views.index)
]

