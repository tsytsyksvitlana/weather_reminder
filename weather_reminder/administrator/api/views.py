from django.core.exceptions import MultipleObjectsReturned
from django.db.models import DateTimeField, ExpressionWrapper, F
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from weather_reminder.administrator.api.serializers import MessageSerializer
from weather_reminder.administrator.models.message import Message
from weather_reminder.exception_handlers.base import EnoughtFailures
from weather_reminder.weather.models.subscription import Subscription


class AdministratorAPIView(generics.GenericAPIView):
    def create_message_failures(self) -> list[Message]:
        """
        Method saves messages to db if there are subscriptions
        that have not been updated 3 times in a row
        """
        current_time = timezone.now()
        subscriptions = (
            Subscription.objects.annotate(
                next_due=ExpressionWrapper(
                    F("last_sent") + F("periodicity") * 3,
                    output_field=DateTimeField(),
                )
            )
            .filter(next_due__lte=current_time)
            .select_related("user", "city")
            .prefetch_related("city__weatherdata")
            .order_by("next_due")
        )

        new_messages = []

        for subscription in subscriptions:
            city = subscription.city
            user = subscription.user
            try:
                message, created = Message.objects.get_or_create(
                    user_id=user.id,
                    city_id=city.id,
                    defaults={"last_sent": subscription.last_sent},
                )
                if created:
                    new_messages.append(message)
            except MultipleObjectsReturned:
                raise EnoughtFailures()

        return new_messages

    def get(self, request: HttpRequest) -> Response:
        """
        Method returns the serialized data of failed subscriptions messages
        """
        try:
            new_messages = self.create_message_failures()
            serializer = MessageSerializer(new_messages, many=True)
            return Response(serializer.data)
        except EnoughtFailures as e:
            return Response({"detail": e.default_detail}, status=e.status_code)
