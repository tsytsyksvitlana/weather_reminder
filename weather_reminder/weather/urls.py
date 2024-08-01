from django.urls import path

from weather_reminder.weather.api.views import SubscribersWeatherDataAPIView
from weather_reminder.weather.views import add_subscription, index


urlpatterns = [
    path("", index, name="index"),
    path("subscription/add/", add_subscription, name="add_subscription"),
    path("api/v1/current-weather/", SubscribersWeatherDataAPIView.as_view()),
]
