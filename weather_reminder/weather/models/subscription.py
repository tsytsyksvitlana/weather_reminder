from datetime import datetime, timezone

from django.db import models

from weather_reminder.celery_config import PERIOD_CHOICES


class Subscription(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["last_sent"]),
            models.Index(fields=["user"]),
            models.Index(fields=["city"]),
        ]

    user = models.ForeignKey("authenticate.User", on_delete=models.CASCADE)
    city = models.ForeignKey("weather.City", on_delete=models.CASCADE)
    periodicity = models.DurationField(choices=PERIOD_CHOICES)
    last_sent = models.DateTimeField(
        verbose_name="last sent", default=datetime.now(timezone.utc)
    )

    def __str__(self):
        return (
            f"Subscription("
            f"id={self.id}, "
            f"user={self.user}, "
            f"city={self.city})"
        )
