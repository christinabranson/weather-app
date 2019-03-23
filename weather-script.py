import requests
import os
import json
key = os.getenv('WEATHER_API_KEY')
if isinstance(key, type(None)):
    print "No API key found"
    os._exit(0)

lat = "39.9526"
lon = "-75.1652"
baseUrl = "https://api.darksky.net/forecast/"
url = baseUrl + key + "/" + lat + "," + lon
print "Calling weather API with URL: " + url
response = requests.get(url)
if response:
    print "Successfully retrieved JSON"
    json_data = json.loads(response.text)
    with open("cached_json.dat", "w") as json_file:
        json.dump(json_data, json_file)
        json_file.close()
else:
    print "Error getting JSON"
    os._exit(0)