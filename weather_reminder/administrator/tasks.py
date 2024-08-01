import os

import requests
from dotenv import load_dotenv

from weather_reminder.core.celery import ScheduledTask, celery_app
from weather_reminder.core.settings import CeleryBeatSchedulers as CBS
from weather_reminder.exception_handlers.base import (
    FetchingFailuresError,
    NotRequiredData,
)


load_dotenv()

ADMIN_TG_CHAT_ID = os.getenv("ADMIN_TG_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def get_message_content(user_id: int, city_id: int, last_sent: str) -> str:
    return (
        f"User ID: {user_id}\n"
        f"City ID: {city_id}\n"
        f"Last Sent: {last_sent}\n"
    )


def get_bot_url(message_text: str) -> str:
    return (
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        f"/sendMessage?chat_id={ADMIN_TG_CHAT_ID}"
        f"&text={message_text}"
    )


@celery_app.task(
    base=ScheduledTask,
    run_every=CBS.check_failures.run_every,
    options={},
    relative=False,
)
def send_messages_to_admin() -> None:
    """
    Function informs the administrator about errors in user subscriptions
    """
    web_host = os.environ.get("WEB_HOST", "web")
    url = f"http://{web_host}:8000/api/v1/failures/weather/"
    response = requests.get(url)

    if response.status_code == 200:
        new_messages = response.json()
        for msg in new_messages:
            if (
                (user_id := msg.get("user_id")) is None
                or (city_id := msg.get("city_id")) is None
                or (last_sent := msg.get("last_sent")) is None
            ):
                raise NotRequiredData()
            message_content = get_message_content(user_id, city_id, last_sent)
            bot_url = get_bot_url(message_content)
            requests.get(bot_url)
    else:
        raise FetchingFailuresError()
