import logging
import os
import typing as t
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal

from django.utils import timezone

import requests
from dotenv import load_dotenv
from typing_extensions import TypedDict

from weather_reminder.authenticate.models.user import User
from weather_reminder.celery_config import TIME_ACCURACY, WEATHER_URL
from weather_reminder.exception_handlers.external_service import (
    ExternalServiceError,
)
from weather_reminder.weather.api.serializers import WeatherDataSubSerializer
from weather_reminder.weather.models.subscription import Subscription
from weather_reminder.weather.models.weather_data import WeatherData


load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

logger = logging.getLogger(__name__)


class WeatherDataDict(TypedDict):
    city: str
    temperature: Decimal
    humidity: int
    wind_speed: Decimal
    weather_description: str
    weather_icon: str
    last_update: t.Optional[timezone.datetime]


def format_weather_data(weather_obj: WeatherData) -> WeatherDataDict:
    return WeatherDataDict(
        city=weather_obj.city.name,
        temperature=weather_obj.temperature,
        humidity=weather_obj.humidity,
        wind_speed=weather_obj.wind_speed,
        weather_description=weather_obj.weather_description,
        weather_icon=weather_obj.weather_icon,
        last_update=weather_obj.last_update,
    )


def weather_url(city: str, country_abbr: str) -> str:
    return (
        f"{WEATHER_URL}/current?&city={city}"
        f"&country={country_abbr}&key={WEATHER_API_KEY}"
    )


def get_weather_data_from_api(
    subscription: Subscription,
) -> WeatherDataDict | None:
    city_instance = subscription.city
    city = city_instance.name
    country_abbr = city_instance.country_abbr
    url = weather_url(city, country_abbr)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data := data.get("data", []):
            data = data[0]
            return WeatherDataDict(
                city=city_instance,
                temperature=Decimal(data["temp"]),
                humidity=data["rh"],
                wind_speed=Decimal(data["wind_spd"]),
                weather_description=data["weather"]["description"],
                weather_icon=data["weather"]["icon"],
                last_update=None,
            )
    elif response.status_code == 400:
        error_data = response.json()
        if (
            "error" in error_data
            and error_data["error"] == "No Location Found. Try lat/lon."
        ):
            return None
    raise ExternalServiceError()


def update_weather_for_subscription(
    subscription: Subscription,
) -> WeatherDataDict | None:
    city = subscription.city
    weather_obj = city.weatherdata.first()
    current_time = timezone.now()
    weather_data = get_weather_data_from_api(subscription)

    if weather_data:
        weather_data["last_update"] = current_time
        if weather_obj:
            for key, value in weather_data.items():
                setattr(weather_obj, key, value)
            weather_obj.save()
        else:
            weather_data_instance = WeatherData(**weather_data)
            weather_data_instance.save()
            weather_obj = weather_data_instance
        return format_weather_data(weather_obj)
    return None


def get_weather_for_user(user: User) -> list[dict[str, str | int]]:
    subscriptions = (
        Subscription.objects.filter(user=user)
        .select_related("city")
        .prefetch_related("city__weatherdata")
    )
    current_time = timezone.now()
    cities_weather_data = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for subscription in subscriptions:
            weather_obj = subscription.city.weatherdata.first()
            if (
                weather_obj
                and (current_time - weather_obj.last_update) <= TIME_ACCURACY
            ):
                weather_data = format_weather_data(weather_obj)
                serialized_data = WeatherDataSubSerializer(data=weather_data)
                if serialized_data.is_valid():
                    cities_weather_data.append(serialized_data.validated_data)
            else:
                futures.append(
                    executor.submit(
                        update_weather_for_subscription, subscription
                    )
                )

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    serialized_data = WeatherDataSubSerializer(data=result)
                    if serialized_data.is_valid():
                        cities_weather_data.append(
                            serialized_data.validated_data
                        )
            except ExternalServiceError:
                logger.error(
                    "External service error occurred while fetching weather data"
                )

    return cities_weather_data
