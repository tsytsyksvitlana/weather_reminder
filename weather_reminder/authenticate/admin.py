from django.contrib import admin

from weather_reminder.authenticate.models.user import User


admin.site.register(User)
