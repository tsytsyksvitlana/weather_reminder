from django.contrib import admin

from weather_reminder.weather.models.city import City
from weather_reminder.weather.models.subscription import Subscription
from weather_reminder.weather.models.weather_data import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ("city", "temperature", "humidity", "last_update")
    list_filter = ("city", "last_update")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country_abbr")
    list_filter = ("name", "country_abbr")
    search_fields = ("name", "country_abbr")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "periodicity", "last_sent")
    list_filter = ("user", "city", "periodicity", "last_sent")
    search_fields = ("user", "city", "last_sent")
