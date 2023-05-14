from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from .serializers import GmtSerializer
from .timeshift_lib import Abstractapi

class Gmt(APIView):
    serializer_class = GmtSerializer

    def get(self, request: Request):
        serializer = self.serializer_class(data=request.query_params)
        if not serializer.is_valid():
            raise ValidationError('Неверный формат названия города.')
        city_name = serializer.data['city_name']

        abstract_api = Abstractapi()
        city_data = abstract_api.find_city(city_name)
        if city_data.get('error'):
            raise ValidationError(f'Город с названием {city_name} не найден.')

        city_data['local_time'] = abstract_api.get_local_time(
            city_data['gmt_offset']
        )
        return Response(city_data)
