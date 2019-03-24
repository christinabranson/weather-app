# This is a script to pull future weather from the Dark Sky weather API (https://darksky.net/dev/docs) and caches them in a file in cached_jason/forecast/cached_json.dat
# Should be run once an hour via cron

import requests
import os
import json
import pytz
from datetime import datetime
import pytz
import time
from datetime import timedelta
from pprint import pprint

key = os.getenv('WEATHER_API_KEY')
if isinstance(key, type(None)):
    print "No API key found"
    os._exit(0)

def getTotalPrecipitation(json_data):
    for dailydata in json_data['daily']['data']:
        #print dailydata['time']
        time = dailydata['time']
        tz = pytz.timezone('America/New_York')
        time = datetime.fromtimestamp(time, tz)
        timeDate = datetime.strftime(time,"%Y-%m-%d")

        with open("cached_data/precipitation/"+timeDate+"_precipitation_amount.dat", "w") as file:
            file.write(str(dailydata['precipIntensity']))
            file.close()
        
lat = "39.9526"
lon = "-75.1652"
baseUrl = "https://api.darksky.net/forecast/"
url = baseUrl + key + "/" + lat + "," + lon
print "Calling weather API with URL: " + url
response = requests.get(url)
if response:
    print "Successfully retrieved JSON"
    json_data = json.loads(response.text)
    getTotalPrecipitation(json_data)
    with open("cached_data/forecast/cached_json.dat", "w") as json_file:
        json.dump(json_data, json_file, sort_keys=True, indent=4)
        json_file.close()
    os._exit(1)
else:
    print "Error getting JSON"
    os._exit(0)