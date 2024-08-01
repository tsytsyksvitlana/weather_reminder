#!/bin/sh

export PYTHONPATH=.

celery -A weather_reminder.core worker -l INFO -Q queue_1
