from rest_framework import serializers

from weather_reminder.administrator.models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages about errors in user subscriptions
    """

    class Meta:
        model = Message
        fields = "__all__"
