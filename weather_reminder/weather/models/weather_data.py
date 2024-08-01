from datetime import datetime, timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WeatherData(models.Model):
    city = models.ForeignKey(
        "weather.City", on_delete=models.CASCADE, related_name="weatherdata"
    )
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    wind_speed = models.DecimalField(
        "wind speed", max_digits=8, decimal_places=2
    )
    weather_description = models.CharField(
        "weather description", max_length=100
    )
    weather_icon = models.CharField("weather icon", max_length=4)
    last_update = models.DateTimeField(
        "last update", default=datetime.now(timezone.utc)
    )

    def __str__(self):
        return (
            f"WeatherData("
            f"city={self.city.name}"
            f"temperature={self.temperature}°C, "
            f"humidity={self.humidity}%, "
            f"wind_speed={self.wind_speed}m/s "
            f"weather_description={self.weather_description} "
            f"weather_icon={self.weather_icon} "
            f"last_update={self.last_update}"
        )
