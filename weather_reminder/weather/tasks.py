import os

from django.core.mail import send_mail

import requests

from weather_reminder.core.celery import ScheduledTask, celery_app
from weather_reminder.core.settings import EMAIL_HOST_USER
from weather_reminder.core.settings import CeleryBeatSchedulers as CBS
from weather_reminder.exception_handlers.external_service import (
    ExternalServiceError,
)
from weather_reminder.weather.api.views import SubscribersWeatherDataAPIView


def get_message_content(
    city: str,
    temperature: float,
    humidity: int,
    wind_speed: float,
    weather_description: str,
) -> str:
    return (
        f"***{city}***:\n"
        f"Temperature: {temperature}°C\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s\n"
        f"Description: {weather_description}\n\n"
    )


@celery_app.task(
    base=ScheduledTask,
    run_every=CBS.send_email.run_every,
    options={},
    relative=False,
    delay=CBS.send_email.delay,
)
def send_weather_to_subscribers() -> None:
    web_host = os.environ.get("WEB_HOST", "web")
    url = f"http://{web_host}:8000/api/v1/current-weather/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for email, cities_weather in data.items():
            message = ""
            for city, weather_data in cities_weather.items():
                message += get_message_content(
                    city=city,
                    temperature=weather_data["temperature"],
                    humidity=weather_data["humidity"],
                    wind_speed=weather_data["wind_speed"],
                    weather_description=weather_data["weather_description"],
                )
            send_mail(
                subject="Your Weather Update",
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )
    else:
        raise ExternalServiceError()


@celery_app.task(
    base=ScheduledTask,
    run_every=CBS.update_weather.run_every,
    options={},
    relative=False,
)
def task_update_weather() -> None:
    SubscribersWeatherDataAPIView().update_weather()
