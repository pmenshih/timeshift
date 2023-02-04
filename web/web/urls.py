from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('timeshift.urls')),
    path('admin/', admin.site.urls),
]
