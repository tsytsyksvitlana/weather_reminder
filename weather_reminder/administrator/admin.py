from django.contrib import admin

from weather_reminder.administrator.models.message import Message


@admin.register(Message)
class CityAdmin(admin.ModelAdmin):
    list_display = ("user_id", "city_id", "last_sent")
    list_filter = ("user_id", "city_id", "last_sent")
    search_fields = ("user_id", "city_id")
