# Generated by Django 5.0.4 on 2024-06-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("user_id", models.IntegerField()),
                ("city_id", models.IntegerField()),
                ("last_sent", models.DateTimeField()),
            ],
        ),
    ]
