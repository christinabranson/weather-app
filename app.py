import os
from flask import Flask
from flask import render_template

from datetime import datetime
import pytz
import time
from datetime import timedelta
from pprint import pprint
from flask import Markup
import collections
from collections import defaultdict


def getPrecipitationData():
    precipData = collections.defaultdict(list)
    tz = pytz.timezone('America/New_York')
    i = 0
    for x in range(-7,7):
        day = str(datetime.strftime(datetime.now(tz=tz) + timedelta(days=x),"%s"))
        dayDate = str(datetime.strftime(datetime.now(tz=tz) + timedelta(days=x),"%Y-%m-%d"))
        dayPretty = str(datetime.strftime(datetime.now(tz=tz) + timedelta(days=x),"%a %d"))
        fileName = "cached_data/precipitation/"+dayDate+"_precipitation_amount.dat"
        if os.path.isfile(fileName):
            i += 1
            file = open(fileName, "r")
            precipData[i].append({'prettyDate': dayPretty})
            precipData[i].append({'precip': file.read()})
    return precipData
    
def getPastWeekPrecipAccumulationData(weather_data):
    accumulation_amount = 0
    precipData = collections.defaultdict(list)
    tz = pytz.timezone('America/New_York')
    currentDayPretty = str(datetime.strftime(datetime.now(tz=tz),"%a %d"))
    i = 0
    hitCurrentDate = 0
    for item in weather_data.values():
        i += 1
        if (item[0]['prettyDate'] == currentDayPretty):
            hitCurrentDate = 1
        if (hitCurrentDate == 0):
            accumulation_amount = accumulation_amount + float(item[1]['precip'])
            precipData[i].append({'prettyDate': item[0]['prettyDate']})
            precipData[i].append({'precip': str(accumulation_amount)})
    return precipData
    
def getPastWeekPrecipAccumulationTotal(weather_data):
    accumulation_amount = 0
    precipData = collections.defaultdict(list)
    tz = pytz.timezone('America/New_York')
    currentDayPretty = str(datetime.strftime(datetime.now(tz=tz),"%a %d"))
    hitCurrentDate = 0
    for item in weather_data.values():
        if (item[0]['prettyDate'] == currentDayPretty):
            hitCurrentDate = 1
        if (hitCurrentDate == 0):
            accumulation_amount = accumulation_amount + float(item[1]['precip'])
    return accumulation_amount

app = Flask(__name__)

@app.route('/')
def showPage():
    # Get the dataset for the full 14 day range
    precipData = getPrecipitationData()
    precipDataKeysString = Markup(', '.join('"' + item[0]['prettyDate'] + '"' for item in precipData.values()))
    precipDataValuesString = (', '.join(item[1]['precip'] for item in precipData.values()))
    
    # Get the past week precipitation acumulation data set
    previousWeekAccumulationData = getPastWeekPrecipAccumulationData(precipData)
    previousWeekAccumulationDataValuesString = (', '.join(item[1]['precip'] for item in previousWeekAccumulationData.values()))
    
    # Get the recommendation based on the data
    previousWeekAccumulationTotal = getPastWeekPrecipAccumulationTotal(precipData)

    hasData = len(precipData)
    return render_template('weather.html', 
        precipArrayKeysString=precipDataKeysString, 
        precipArrayValuesString=precipDataValuesString, 
        previousWeekAccumulationDataValuesString=previousWeekAccumulationDataValuesString, 
        previousWeekAccumulationTotal = previousWeekAccumulationTotal,
        hasData = hasData
    )

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))