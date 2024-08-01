# Generated by Django 5.0.4 on 2024-05-26 21:07

import datetime

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("country_abbr", models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "periodicity",
                    models.DurationField(
                        choices=[
                            (
                                datetime.timedelta(seconds=600),
                                "Every 10 minutes",
                            ),
                            (datetime.timedelta(seconds=3600), "Every hour"),
                            (
                                datetime.timedelta(seconds=43200),
                                "Every 12 hours",
                            ),
                            (datetime.timedelta(days=1), "Every 24 hours"),
                        ]
                    ),
                ),
                (
                    "last_sent",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2024,
                            5,
                            26,
                            21,
                            6,
                            46,
                            684379,
                            tzinfo=datetime.timezone.utc,
                        )
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="weather.city",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WeatherData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "temperature",
                    models.DecimalField(decimal_places=1, max_digits=5),
                ),
                (
                    "humidity",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                (
                    "wind_speed",
                    models.DecimalField(decimal_places=2, max_digits=8),
                ),
                ("weather_description", models.CharField(max_length=100)),
                ("weather_icon", models.CharField(max_length=4)),
                (
                    "last_update",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2024,
                            5,
                            26,
                            21,
                            6,
                            46,
                            733359,
                            tzinfo=datetime.timezone.utc,
                        )
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weatherdata",
                        to="weather.city",
                    ),
                ),
            ],
        ),
    ]