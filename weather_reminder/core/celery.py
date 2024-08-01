import os

from celery import Celery, Task
from kombu import Queue


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "weather_reminder.core.settings"
)

celery_app = Celery("core")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")


celery_app.autodiscover_tasks()

celery_app.conf.task_queues = (
    Queue("queue_1", routing_key="task_1"),
    Queue("queue_2", routing_key="task_2"),
)

celery_app.conf.task_routes = {
    "weather_reminder.weather.tasks.send_weather_to_subscribers": {
        "queue": "queue_1"
    },
    "weather_reminder.weather.tasks.task_update_weather": {"queue": "queue_2"},
}


class ScheduledTask(Task):
    delay = 300

    @classmethod
    def on_bound(cls, celery_app: Celery):
        celery_app.conf.beat_schedule[cls.name] = {
            "task": cls.name,
            "schedule": cls.run_every,
            "args": (),
            "kwargs": {},
            "options": cls.options or {},
            "relative": cls.relative,
        }

    @classmethod
    def schedule_task(cls):
        cls.apply_async(countdown=cls.delay)
