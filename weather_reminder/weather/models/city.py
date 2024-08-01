from django.db import models


class City(models.Model):
    name = models.CharField("city name", max_length=50)
    country_abbr = models.CharField("country abbreviation", max_length=4)

    def __str__(self):
        return (
            f"City("
            f"id={self.id}, "
            f"name={self.name}, "
            f"country_abbr={self.country_abbr})"
        )
