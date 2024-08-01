import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.db.models import DateTimeField, ExpressionWrapper, F
from django.utils import timezone
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from weather_reminder.celery_config import TIME_ACCURACY
from weather_reminder.weather.api.serializers import WeatherDataSubSerializer
from weather_reminder.weather.functions import (
    format_weather_data,
    get_weather_data_from_api,
)
from weather_reminder.weather.models.subscription import Subscription
from weather_reminder.weather.models.weather_data import WeatherData


logger = logging.getLogger(__name__)


class SubscribersWeatherDataAPIView(generics.GenericAPIView):
    def get_queryset(self):
        current_time = timezone.now()
        subscriptions = (
            Subscription.objects.annotate(
                next_due=ExpressionWrapper(
                    F("last_sent") + F("periodicity"),
                    output_field=DateTimeField(),
                )
            )
            .filter(next_due__lte=current_time)
            .select_related("user", "city")
            .prefetch_related("city__weatherdata")
            .order_by("next_due")
        )
        return subscriptions

    def get_weather_to_send(self):
        """
        Method returns weather data from db that doesn't need update
        """
        current_time = timezone.now()
        subscriptions = self.get_queryset().filter(
            city__weatherdata__last_update__gte=current_time - TIME_ACCURACY
        )
        users_weather_data = {}

        def process_subscription(subscription):
            """
            Function takes a subscription and returns weather data
            """
            city = subscription.city
            weather_obj = city.weatherdata.first()
            weather_data = format_weather_data(weather_obj)
            weather_data["city"] = city.name

            serializer = WeatherDataSubSerializer(data=weather_data)
            if serializer.is_valid():
                subscription.last_sent = current_time
                user_email = subscription.user.email
                if user_email not in users_weather_data:
                    users_weather_data[user_email] = {}
                users_weather_data[user_email][city.name] = serializer.data
            else:
                logger.error(f"Serializer Errors: {serializer.errors}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(process_subscription, subscription)
                for subscription in subscriptions
            ]
            for future in as_completed(futures):
                future.result()

        subscriptions.update(last_sent=current_time)
        return users_weather_data

    def fetch_and_update_weather(
        self, subscription: Subscription
    ) -> WeatherDataSubSerializer:
        """
        Method updates weather data for concrete subscription
        """
        city = subscription.city
        weather_obj = city.weatherdata.first()
        weather_data = get_weather_data_from_api(subscription)
        if weather_data:
            weather_data["city"] = city
            weather_data["last_update"] = timezone.now()
            if weather_obj:
                for key, value in weather_data.items():
                    setattr(weather_obj, key, value)
                weather_obj.save()
            else:
                WeatherData.objects.create(**weather_data)
            weather_data_formatted = format_weather_data(
                WeatherData(**weather_data)
            )
            return WeatherDataSubSerializer(
                weather_data_formatted, subscription
            )

    def update_weather(self, max_workers=4):
        """
        Method updates weather data for subscriptions to send
        """
        current_time = timezone.now()
        subscriptions = self.get_queryset().filter(
            city__weatherdata__last_update__lt=current_time - TIME_ACCURACY
        )
        cities_weather_data = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.fetch_and_update_weather, subscription)
                for subscription in subscriptions
            ]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    cities_weather_data.append(result)

        return cities_weather_data

    def get(self, request: Request) -> Response:
        weather_data = self.get_weather_to_send()
        return Response(weather_data)
