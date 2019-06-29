from django.db import models
from django.conf import settings
from django.utils.timezone import now

class WeatherData(models.Model):
    date = models.DateTimeField(default=now, blank=True)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
    class Meta:
        ordering = ['date']

class ManualWeatherData(models.Model):
    date = models.DateTimeField(default=now, blank=True)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
    class Meta:
        ordering = ['date']