# This is a script to pull the last 7 previous day's weather from the Dark Sky weather API
# (https://darksky.net/dev/docs) and saves in the database
# Should be run once manually to initialize past data. After inital run, the single-previous-weather-script.py script
# should handle updates
# Run with `python manage.py future_weather`

from django.core.management.base import BaseCommand
import logging
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info("server.management.commands.clear_all_weather")

        with connection.cursor() as cursor:
            cursor.execute("delete from server_weatherdata", [])
            cursor.execute("delete from server_manualweatherdata", [])