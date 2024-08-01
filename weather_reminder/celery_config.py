from datetime import timedelta


PERIOD_CHOICES = [
    (timedelta(minutes=10), "Every 10 minutes"),
    (timedelta(hours=1), "Every hour"),
    (timedelta(hours=12), "Every 12 hours"),
    (timedelta(hours=24), "Every 24 hours"),
]
WEATHER_URL = "https://api.weatherbit.io/v2.0"
TIME_ACCURACY = timedelta(minutes=5)
