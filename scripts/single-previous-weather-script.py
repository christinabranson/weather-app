# This is a script to pull previous day's weather from the Dark Sky weather API (https://darksky.net/dev/docs) and caches them in a file in cached_jason/previous/{datetime}_cached_json.dat
# Should be run once "today" to get the previous day's data via cron

import requests
import os
import json
from datetime import datetime
import pytz
import time
from datetime import timedelta
from pprint import pprint

def getTotalPrecipitation(json_data, yesterdayDate):
    preciptationSum = 0
    for hourlydata in json_data['hourly']['data']:
        print hourlydata['precipIntensity']
        preciptationSum += hourlydata['precipIntensity']
    
    with open("cached_data/precipitation/"+yesterdayDate+"_precipitation_amount.dat", "w") as file:
        file.write(str(preciptationSum))
        file.close()

key = os.getenv('WEATHER_API_KEY')
if isinstance(key, type(None)):
    print "No API key found"
    os._exit(0)

lat = "39.9526"
lon = "-75.1652"
baseUrl = "https://api.darksky.net/forecast/"
#yesterday = (date.today() - timedelta(days=1))
tz = pytz.timezone('America/New_York')
yesterday = str(datetime.strftime(datetime.now(tz=tz) - timedelta(days=1),"%s"))
yesterdayDate = str(datetime.strftime(datetime.now(tz=tz) - timedelta(days=1),"%Y-%m-%d"))
url = baseUrl + key + "/" + lat + "," + lon + "," + yesterday + "?exclude=daily,currently,flags,minutely,alerts"
print "Calling weather API with URL: " + url
response = requests.get(url)
if response:
    print "Successfully retrieved JSON"
    json_data = json.loads(response.text)
    getTotalPrecipitation(json_data, yesterdayDate)
    with open("cached_data/previous/"+yesterdayDate+"_cached_json.dat", "w") as json_file:
        json.dump(json_data, json_file, sort_keys=True, indent=4)
        json_file.close()
    os._exit(1)
else:
    print "Error getting JSON"
    os._exit(0)