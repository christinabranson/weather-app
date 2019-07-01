# This is a script to pull previous day's weather from the Dark Sky weather API (https://darksky.net/dev/docs)
# and saves in the database
# Should be run once "today" to get the previous day's data via cron
# Run with `python manage.py previous_weather_single`

from django.core.management.base import BaseCommand
import logging
from django.conf import settings
from datetime import datetime, timedelta, time
import pytz
import requests
import os
import json
from server.models import WeatherData

class Command(BaseCommand):

    def getDailyTotalPrecipitation(self, json_data):
        preciptationSum = 0
        for hourlydata in json_data['hourly']['data']:
            preciptationSum += hourlydata['precipIntensity']

        return preciptationSum

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info("server.management.commands.previous_weather_single")

        key = settings.DARK_SKY_API_KEY
        lat = settings.DARK_SKY_API_LAT
        lon = settings.DARK_SKY_API_LON

        baseUrl = "https://api.darksky.net/forecast/"
        tz = pytz.timezone('America/New_York')

        time_now = datetime.now(tz=tz).date()
        time_midnight = tz.localize(datetime.combine(time_now, time(0, 0)), is_dst=None)
        logger.debug(time_now)
        logger.debug(time_midnight)

        x = 1 # yesterday
        timestamp = int(datetime.timestamp(time_midnight - timedelta(days=x)))
        logger.debug(timestamp)

        url = baseUrl + key + "/" + lat + "," + lon + "," + str(timestamp) + "?exclude=daily,currently,flags,minutely,alerts"

        logger.info("Calling URL: " + url)

        response = requests.get(url)
        if response:
            logger.info("Successfully retrieved JSON")
            json_data = json.loads(response.text)
            logger.debug(json_data)
            dailyPrecipTotal = self.getDailyTotalPrecipitation(json_data)

            model_datetime = datetime.fromtimestamp(timestamp, tz=tz)

            daily_precip = WeatherData.objects.get_or_create(date=model_datetime)[0]
            daily_precip.precip_amount = dailyPrecipTotal
            daily_precip.save()
        else:
            logger.error("Failed retrieving JSON")