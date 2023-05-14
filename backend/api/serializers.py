from rest_framework import serializers

class GmtSerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=50, required=True)
