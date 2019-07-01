# This is a script to pull the last 7 previous day's weather from the Dark Sky weather API
# (https://darksky.net/dev/docs) and saves in the database
# Should be run once manually to initialize past data. After inital run, the single-previous-weather-script.py script
# should handle updates
# Run with `python manage.py future_weather`

from django.core.management.base import BaseCommand
import logging
from django.conf import settings
from datetime import datetime, timedelta, time
from datetime import time as customtime
import pytz
import requests
import os
import json
from server.models import WeatherData

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info("server.management.commands.future_weather")

        key = settings.DARK_SKY_API_KEY
        lat = settings.DARK_SKY_API_LAT
        lon = settings.DARK_SKY_API_LON

        baseUrl = "https://api.darksky.net/forecast/"
        tz = pytz.timezone('America/New_York')

        time_now = datetime.now(tz=tz).date()
        time_midnight = tz.localize(datetime.combine(time_now, customtime(0, 0)), is_dst=None)
        logger.debug(time_now)
        logger.debug(time_midnight)

        url = url = baseUrl + key + "/" + lat + "," + lon

        logger.info("Calling URL: " + url)

        response = requests.get(url)
        if response:
            logger.info("Successfully retrieved JSON")
            json_data = json.loads(response.text)
            logger.debug(json_data)
            for dailydata in json_data['daily']['data']:
                # print dailydata['time']
                time = dailydata['time']
                tz = pytz.timezone('America/New_York')
                model_datetime = model_datetime = datetime.fromtimestamp(time, tz=tz)

                daily_precip = WeatherData.objects.get_or_create(date=model_datetime)[0]
                daily_precip.precip_amount = dailydata['precipIntensity']
                daily_precip.save()
        else:
            logger.error("Failed retrieving JSON")