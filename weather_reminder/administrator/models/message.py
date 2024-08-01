from django.core.validators import MinValueValidator
from django.db import models


class Message(models.Model):
    """
    Class for storing information for the administrator about errors
    in user subscriptions
    """

    class Meta:
        app_label = "administrator"

    user_id = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    city_id = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    last_sent = models.DateTimeField(verbose_name="last sent")

    def __str__(self):
        return (
            f"Message(id={self.id}, "
            f"email={self.user_id}, "
            f"city_id={self.city_id}, "
            f"last_sent={self.last_sent})"
        )
