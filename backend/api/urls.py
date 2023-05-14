from django.urls import path

from .views import Gmt

urlpatterns = [
    path('gmt/', Gmt.as_view())
]

