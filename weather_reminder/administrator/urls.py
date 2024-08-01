from django.urls import path

from weather_reminder.administrator.api.views import AdministratorAPIView


urlpatterns = [
    path("api/v1/failures/weather/", AdministratorAPIView.as_view()),
]
