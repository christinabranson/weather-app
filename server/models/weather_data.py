from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class WeatherData(models.Model):
    datetime = models.IntegerField(blank=False, null=False)
    precip_amount = models.FloatField(default=0, blank=False, null=False)

class ManualWeatherData(models.Model):
    datetime = models.DateTimeField(blank=False, null=False)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
