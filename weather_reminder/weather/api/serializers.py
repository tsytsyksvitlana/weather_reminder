from rest_framework import serializers


class WeatherDataSubSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
    wind_speed = serializers.FloatField()
    weather_description = serializers.CharField()
    weather_icon = serializers.CharField()
    last_update = serializers.DateTimeField()
