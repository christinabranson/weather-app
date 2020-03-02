from django.db import models
from django.conf import settings
from django.utils.timezone import now
import pytz

class WeatherData(models.Model):
    date = models.DateTimeField(default=now, blank=True)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
    class Meta:
        ordering = ['date']

    @staticmethod
    def future_weather():
        from django.conf import settings
        from datetime import datetime, timedelta, time
        from datetime import time as customtime
        import pytz
        import requests
        import os
        import json
        from server.models import WeatherData

        key = settings.DARK_SKY_API_KEY
        lat = settings.DARK_SKY_API_LAT
        lon = settings.DARK_SKY_API_LON

        baseUrl = "https://api.darksky.net/forecast/"
        tz = pytz.timezone('America/New_York')

        time_now = datetime.now(tz=tz).date()
        time_midnight = tz.localize(datetime.combine(time_now, customtime(0, 0)), is_dst=None)

        url = url = baseUrl + key + "/" + lat + "," + lon

        response = requests.get(url)
        if response:
            json_data = json.loads(response.text)
            for dailydata in json_data['daily']['data']:
                # print dailydata['time']
                time = dailydata['time']
                tz = pytz.timezone('America/New_York')
                model_datetime = model_datetime = datetime.fromtimestamp(time, tz=tz)

                daily_precip = WeatherData.objects.get_or_create(date=model_datetime)[0]
                daily_precip.precip_amount = dailydata['precipIntensity']
                daily_precip.save()
            return "yay"
        else:
            return "fail"

    @staticmethod
    def get_at_a_glance():
        from datetime import datetime, timedelta, time
        from django.db.models import Sum
        import math
        import json

        data_array = {}
        data_array["summary"] = {}
        data_array["summary"]["last_week"] = {}
        data_array["summary"]["next_week"] = {}
        data_array["summary"]["last_day"] = {}
        data_array["summary"]["next_day"] = {}
        data_array["summary"]["recommendation"] = {}

        data_array["data"] = []

        startDays = 7
        endDays = 7

        tz = pytz.timezone('America/New_York')
        time_now = datetime.now(tz=tz).date()
        time_midnight = tz.localize(datetime.combine(time_now, time(0, 0)), is_dst=None)
        start = time_midnight - timedelta(days=startDays)
        end = time_midnight + timedelta(days=endDays)
        next_2 = time_midnight + timedelta(days=1)
        last_day = time_midnight - timedelta(days=1)

        data_array["summary"]["date_created"] = datetime.strftime(datetime.now(tz=tz), "%m/%d/%Y, %H:%M:%S")

        agg_weather_data_past = WeatherData.objects.filter(date__gte=start).filter(date__lte=time_midnight).aggregate(total_accumulation=Sum('precip_amount'))
        agg_manual_weather_data_past = ManualWeatherData.objects.filter(date__gte=start).filter(date__lte=time_midnight).aggregate(total_accumulation=Sum('precip_amount'))

        agg_weather_data_past_day = WeatherData.objects.filter(date__gte=last_day).filter(date__lte=time_midnight).aggregate(total_accumulation=Sum('precip_amount'))
        agg_manual_weather_data_past_day = ManualWeatherData.objects.filter(date__gte=last_day).filter(date__lte=time_midnight).aggregate(total_accumulation=Sum('precip_amount'))

        agg_weather_data_forecast = WeatherData.objects.filter(date__gte=time_midnight).filter(date__lte=end).aggregate(total_accumulation=Sum('precip_amount'))
        agg_weather_data_forecast_next_day = WeatherData.objects.filter(date__gte=time_midnight).filter(date__lte=next_2).aggregate(total_accumulation=Sum('precip_amount'))

        # get last week data
        data_array["summary"]["last_week"]["start"] = start
        data_array["summary"]["last_week"]["stop"] = time_midnight
        if agg_weather_data_past is not None and agg_weather_data_past['total_accumulation'] is not None:
            data_array["summary"]["last_week"]["rain"] = round(float(agg_weather_data_past['total_accumulation']),2)
        else:
            data_array["summary"]["last_week"]["rain"] = 0

        if agg_manual_weather_data_past is not None and agg_manual_weather_data_past['total_accumulation'] is not None:
            data_array["summary"]["last_week"]["manual"] = round(float(agg_manual_weather_data_past['total_accumulation']),2)
        else:
            data_array["summary"]["last_week"]["manual"] = 0

        data_array["summary"]["last_week"]["total"] = data_array["summary"]["last_week"]["rain"] + data_array["summary"]["last_week"]["manual"]

        # get next week forecast data
        data_array["summary"]["next_week"]["start"] = time_midnight
        data_array["summary"]["next_week"]["stop"] = end
        if agg_weather_data_forecast is not None and agg_weather_data_forecast['total_accumulation'] is not None:
            data_array["summary"]["next_week"]["rain"] = float(agg_weather_data_forecast['total_accumulation'])
        else:
            data_array["summary"]["next_week"]["rain"] = 0

        data_array["summary"]["next_week"]["total"] = data_array["summary"]["next_week"]["rain"]

        # get last day data
        data_array["summary"]["last_day"]["start"] = last_day
        data_array["summary"]["last_day"]["stop"] = time_midnight
        if agg_weather_data_past_day is not None and agg_weather_data_past_day['total_accumulation'] is not None:
            data_array["summary"]["last_day"]["rain"] = round(float(agg_weather_data_past_day['total_accumulation']),2)
        else:
            data_array["summary"]["last_day"]["rain"] = 0

        if agg_manual_weather_data_past_day is not None and agg_manual_weather_data_past_day['total_accumulation'] is not None:
            data_array["summary"]["last_day"]["manual"] = round(float(agg_manual_weather_data_past_day['total_accumulation']),2)
        else:
            data_array["summary"]["last_day"]["manual"] = 0

        data_array["summary"]["last_day"]["total"] = data_array["summary"]["last_day"]["rain"] + data_array["summary"]["last_day"]["manual"]

        # get next day forecast data
        data_array["summary"]["next_day"]["start"] = time_midnight
        data_array["summary"]["next_day"]["stop"] = next_2
        if agg_weather_data_forecast_next_day is not None and agg_weather_data_forecast_next_day['total_accumulation'] is not None:
            data_array["summary"]["next_day"]["rain"] = round(float(agg_weather_data_forecast_next_day['total_accumulation']),2)
        else:
            data_array["summary"]["next_day"]["rain"] = 0

        data_array["summary"]["next_day"]["total"] = data_array["summary"]["next_day"]["rain"]

        # now calculate recommendation
        # todo: flesh out the logic here
        if data_array["summary"]["last_day"]["total"] > 1:
            data_array["summary"]["recommendation"]["bool"] = False
            data_array["summary"]["recommendation"]["message"] = "It has rained more than 1 inch in the last day"
        else:
            data_array["summary"]["recommendation"]["bool"] = True
            data_array["summary"]["recommendation"]["message"] = "It hasn't rained more than 1 inch in the last day"

        weather_data = WeatherData.objects.filter(date__gte=start).filter(date__lte=end)
        manually_weather_data = ManualWeatherData.objects.filter(date__gte=start).filter(date__lte=end)

        startDaysNeg = -1 * startDays
        for x in range(startDaysNeg, endDays):
            day = time_midnight + timedelta(days=x)

            data = {}
            data["num"] = x
            data["labels"] = {}
            data["data"] = {}

            data["labels"]["label"] = datetime.strftime(day, "%d %B | %A")
            data["labels"]["label_short"] = datetime.strftime(day, "%a, %d %b")
            data["labels"]["day"] = datetime.strftime(day, "%A")
            data["labels"]["day_short"] = datetime.strftime(day, "%a")
            data["labels"]["date"] = datetime.strftime(day, "%d %B")
            data["labels"]["date_short"] = datetime.strftime(day, "%d %b")

            # get weather data
            qs_day_weather_data = weather_data.filter(
                date__year=datetime.strftime(day, "%Y"),
                date__month=datetime.strftime(day, "%m"),
                date__day=datetime.strftime(day, "%d")
            )
            if qs_day_weather_data.count() > 0:
                day_weather_data = qs_day_weather_data[0]
                data["data"]["rain"] = round(day_weather_data.precip_amount,2)
            else:
                data["data"]["rain"] = 0

            # get manual weather data
            # this assumes only 1 manual weather; seems ok to me
            qs_day_manual_weather_data = manually_weather_data.filter(
                date__year=datetime.strftime(day, "%Y"),
                date__month=datetime.strftime(day, "%m"),
                date__day=datetime.strftime(day, "%d")
            )
            if qs_day_manual_weather_data.count() > 0:
                day_manual_weather_data = qs_day_manual_weather_data[0]
                data["data"]["manual"] = round(day_manual_weather_data.precip_amount, 2)
            else:
                data["data"]["manual"] = 0

            data["data"]["total"] = data["data"]["rain"] + data["data"]["manual"]


            data_array["data"].append(data)

        # Write to file
        with open("frontend/static/frontend/data_at_a_glance.json", "w") as json_file:
            json.dump(data_array, json_file, sort_keys=True, indent=4, default=str)
            json_file.close()

        return data_array

    @staticmethod
    def get_kitchen_sink():
        from datetime import datetime, timedelta, time
        from django.db.models import Sum
        import math
        import json

        data_array = {}
        data_array["summary"] = {}
        data_array["data"] = []

        startDays = 4
        endDays = 5

        tz = pytz.timezone('America/New_York')
        time_now = datetime.now(tz=tz).date()
        time_midnight = tz.localize(datetime.combine(time_now, time(0, 0)), is_dst=None)
        start = time_midnight - timedelta(days=startDays)
        end = time_midnight + timedelta(days=endDays)

        data_array["summary"]["date_created"] = datetime.strftime(datetime.now(tz=tz), "%m/%d/%Y, %H:%M:%S")

        weather_data = WeatherData.objects.filter(date__gte=start).filter(date__lte=end)
        manually_weather_data = ManualWeatherData.objects.filter(date__gte=start).filter(date__lte=end)

        weather_data_agg = WeatherData.objects.filter(date__gte=start).filter(date__lte=end).aggregate(total_accumulation=Sum('precip_amount'))
        manual_weather_data_agg = ManualWeatherData.objects.filter(date__gte=start).filter(date__lte=end).aggregate(total_accumulation=Sum('precip_amount'))

        total_accumulation = 0
        if weather_data_agg is not None and weather_data_agg['total_accumulation'] is not None:
            total_accumulation = total_accumulation + float(weather_data_agg['total_accumulation'])
        if manual_weather_data_agg is not None and manual_weather_data_agg['total_accumulation'] is not None:
            total_accumulation = total_accumulation + float(manual_weather_data_agg['total_accumulation'])

        data_array["summary"]["total_accumulation_actual"] = total_accumulation
        data_array["summary"]["total_accumulation"] = math.ceil(total_accumulation)

        startDaysNeg = -1*startDays
        accumulation = 0
        reached_today = False
        reached_tomorrow = False
        previous_week_accumulation = 0
        next_day_forecast_accumulation = 0
        for x in range(startDaysNeg, endDays):
            day = time_midnight + timedelta(days=x)

            data = {}

            data["label"] = datetime.strftime(day, "%A, %d %B")
            data["label_short"] = datetime.strftime(day, "%a, %d %b")
            data["day"] = datetime.strftime(day, "%A")
            data["day_short"] = datetime.strftime(day, "%a")
            data["date"] = datetime.strftime(day, "%d %B")
            data["date_short"] = datetime.strftime(day, "%d %b")
            data["tooltiplabel"] = datetime.strftime(day, "%d%m%Y")

            data["amount_accumulation"] = round(accumulation, 2)

            # get weather data
            qs_day_weather_data = weather_data.filter(
                date__year=datetime.strftime(day, "%Y"),
                date__month=datetime.strftime(day, "%m"),
                date__day=datetime.strftime(day, "%d")
            )
            if qs_day_weather_data.count() > 0:
                day_weather_data = qs_day_weather_data[0]
                data["amount_rain"] = round(day_weather_data.precip_amount, 2)
                accumulation += day_weather_data.precip_amount
            else:
                data["amount_rain"] = 0

            # this assumes only 1 manual weather; seems ok to me
            qs_day_manual_weather_data = manually_weather_data.filter(
                date__year=datetime.strftime(day, "%Y"),
                date__month=datetime.strftime(day, "%m"),
                date__day=datetime.strftime(day, "%d")
            )
            if qs_day_manual_weather_data.count() > 0:
                day_manual_weather_data = qs_day_manual_weather_data[0]
                data["amount_manual"] = round(day_manual_weather_data.precip_amount, 2)
                accumulation += day_manual_weather_data.precip_amount
            else:
                data["amount_manual"] = 0

            if data_array["summary"]["total_accumulation"] > 0:
                data["percent_rain"] = round(data["amount_rain"] / data_array["summary"]["total_accumulation"] * 100, 2)
                data["percent_manual"] = round(data["amount_manual"] / data_array["summary"]["total_accumulation"] * 100, 2)
                data["percent_accumulation"] = round(data["amount_accumulation"] / data_array["summary"]["total_accumulation"] * 100, 2)
                data["percent_empty"] = round(100 - data["percent_rain"] - data["percent_manual"] - data["percent_accumulation"], 2)
            else:
                data["percent_rain"] = 0
                data["percent_manual"] = 0
                data["percent_accumulation"] = 0
                data["percent_empty"] = 0

            # change them to a string and add the percentages
            for variable in {"percent_rain", "percent_manual", "percent_accumulation", "percent_empty"}:
                data[variable] = str(data[variable]) + "%"

            data["today"] = 0
            data["today_class"] = ""
            if datetime.strftime(day, "%d") == datetime.strftime(time_now, "%d"):
                reached_today = True
                previous_week_accumulation = round(accumulation, 2)
                data["today"] = 1
                data["today_class"] = "today"
            else:
                if reached_today and not reached_tomorrow:
                    reached_tomorrow = True
                    next_day_forecast_accumulation = data["amount_rain"]

            data_array["data"].append(data)

        data_array["summary"]["previous_week_accumulation"] = previous_week_accumulation
        data_array["summary"]["next_day_forecast_accumulation"] = next_day_forecast_accumulation

        # Now do the logic of whether we should water this week or not
        if previous_week_accumulation >= 1:
            data_array["summary"]["should_water"] = False
            data_array["summary"]["should_water_message"] = "We've already reached " + str(round(previous_week_accumulation, 2)) + "in of rain this week. This meets our weekly goal of 1 inch per week."
        else:
            if previous_week_accumulation + next_day_forecast_accumulation >= 1:
                data_array["summary"]["should_water"] = False
                data_array["summary"]["should_water_message"] = "We've already reached " + str(round(previous_week_accumulation, 2)) + "in of rain this week and we're expecting another " + str(round(next_day_forecast_accumulation, 2)) + "in tomorrow. This meets our weekly goal of 1 inch per week."
            else:
                data_array["summary"]["should_water"] = True
                data_array["summary"]["should_water_message"] = "We've only reached " + str(round(previous_week_accumulation, 2)) + "in of rain this week. This doesn't meet our weekly goal of 1 inch per week."

        data_array["summary"]["should_water_formatted"] = "Yes!" if data_array["summary"]["should_water"] else "No!"

        # Write to file
        with open("frontend/static/frontend/data_kitchen_sink.json", "w") as json_file:
            json.dump(data_array, json_file, sort_keys=True, indent=4)
            json_file.close()

        return data_array

class ManualWeatherData(models.Model):
    date = models.DateTimeField(default=now, blank=True)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
    class Meta:
        ordering = ['date']