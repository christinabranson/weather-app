import os
from flask import Flask
from flask import render_template

from datetime import datetime
import pytz
import time
from datetime import timedelta
from pprint import pprint
from flask import Markup

def getPrecipitationData():
    precipArray = {}
    tz = pytz.timezone('America/New_York')
    for x in range(-7,7):
        day = str(datetime.strftime(datetime.now(tz=tz) + timedelta(days=x),"%s"))
        dayDate = str(datetime.strftime(datetime.now(tz=tz) + timedelta(days=x),"%Y-%m-%d"))
        dayPretty = str(datetime.strftime(datetime.now(tz=tz) + timedelta(days=x),"%a %d"))
        fileName = "cached_data/precipitation/"+dayDate+"_precipitation_amount.dat"
        if os.path.isfile(fileName):
            file = open(fileName, "r")
            precipArray[dayPretty] = file.read()
    return precipArray

app = Flask(__name__)

@app.route('/')
def showPage():
    precipArray = getPrecipitationData()
    precipArrayKeysString = Markup(', '.join('\'' + item + '\'' for item in precipArray.keys()))
    precipArrayValuesString = (','.join(map(str, precipArray.values())))
    hasData = len(precipArray)
    return render_template('weather.html', precipArrayKeysString=precipArrayKeysString, precipArrayValuesString=precipArrayValuesString, hasData = hasData)

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))