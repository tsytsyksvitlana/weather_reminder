from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("weather_reminder.authenticate.urls")),
    path("", include("weather_reminder.weather.urls")),
    path("", include("weather_reminder.administrator.urls")),
]
