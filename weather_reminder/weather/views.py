import logging

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

import requests

from weather_reminder.authenticate.models.user import User
from weather_reminder.celery_config import PERIOD_CHOICES
from weather_reminder.weather.functions import get_weather_for_user, weather_url
from weather_reminder.weather.models.city import City
from weather_reminder.weather.models.subscription import Subscription


logger = logging.getLogger(__name__)


def index(request: HttpRequest) -> HttpResponse:
    if (
        request.user.is_anonymous
        or (user := User.objects.filter(id=request.user.id).first()) is None
    ):
        return redirect("login")
    cities_weather_data = get_weather_for_user(user)
    return render(request, "index.html", {"weather_data": cities_weather_data})


def validate(request: HttpRequest, city_name: str, country_abbr: str) -> bool:
    url = weather_url(city_name, country_abbr)
    response = requests.get(url)
    logger.info(response.text)
    if response.status_code == 200:
        return True
    elif response.status_code == 400:
        error_data = response.json()
        if (
            "error" in error_data
            and error_data["error"] == "No Location Found. Try lat/lon."
        ):
            return False
    return False


def add_subscription(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        city_name = request.POST.get("city")
        country_abbr = request.POST.get("country_abbr")
        periodicity = request.POST.get("periodicity")

        if not all([city_name, country_abbr, periodicity]):
            messages.error(request, "Please enter all fields!")
            return redirect("add_subscription")

        if city_name is None or country_abbr is None:
            messages.error(
                request, "City and country abbreviation cannot be empty."
            )
            return redirect("add_subscription")

        if not validate(request, city_name, country_abbr):
            messages.error(request, "No Location Found.")
            return redirect("add_subscription")

        user = request.user
        city, _ = City.objects.get_or_create(
            name=city_name, country_abbr=country_abbr
        )
        _, created = Subscription.objects.get_or_create(
            city=city, user=user, periodicity=periodicity
        )
        if not created:
            messages.error(
                request, "Subscription for this city already exists."
            )
            return redirect("add_subscription")
        return redirect("index")

    return render(
        request,
        "add_subscription.html",
        {"periodicity_choices": PERIOD_CHOICES},
    )
