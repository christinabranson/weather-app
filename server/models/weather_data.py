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
    def get_kitchen_sink():
        from datetime import datetime, timedelta, time
        from django.db.models import Sum
        import math
        import json

        data_array = {}
        data_array["summary"] = {}
        data_array["data"] = []

        startDays = 5
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

            data["label"] = datetime.strftime(day, "%A, %-d %B")
            data["day"] = datetime.strftime(day, "%A")
            data["date"] = datetime.strftime(day, "%-d %B")
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
                data["amount_rain"] = day_weather_data.precip_amount
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
                data["amount_manual"] = day_manual_weather_data.precip_amount
                accumulation += day_manual_weather_data.precip_amount
            else:
                data["amount_manual"] = 0

            data["percent_rain"] = round(data["amount_rain"] / data_array["summary"]["total_accumulation"] * 100, 2)
            data["percent_manual"] = round(data["amount_manual"] / data_array["summary"]["total_accumulation"] * 100, 2)
            data["percent_accumulation"] = round(data["amount_accumulation"] / data_array["summary"]["total_accumulation"] * 100, 2)
            data["percent_empty"] = round(100 - data["percent_rain"] - data["percent_manual"] - data["percent_accumulation"], 2)

            # change them to a string and add the percentages
            for variable in {"percent_rain", "percent_manual", "percent_accumulation", "percent_empty"}:
                data[variable] = str(data[variable]) + "%"

            data["today"] = 0
            if datetime.strftime(day, "%-d") == datetime.strftime(time_now, "%-d"):
                reached_today = True
                previous_week_accumulation = round(accumulation, 2)
                data["today"] = 1
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
            data_array["summary"]["should_water_message"] = "We've already reached " + str(round(previous_week_accumulation, 2)) + " inch(es) of rain this week. This meets our weekly goal of 1 inch per week."
        else:
            if previous_week_accumulation + next_day_forecast_accumulation >= 1:
                data_array["summary"]["should_water"] = False
                data_array["summary"]["should_water_message"] = "We've already reached " + str(round(previous_week_accumulation, 2)) + " inch(es) of rain this week and we're expecting another " + str(round(next_day_forecast_accumulation, 2)) + " inch(es) tomorrow. This meets our weekly goal of 1 inch per week."
            else:
                data_array["summary"]["should_water"] = True
                data_array["summary"]["should_water_message"] = "We've only reached " + str(round(previous_week_accumulation, 2)) + " inch(es) of rain this week. This doesn't meet our weekly goal of 1 inch per week."

        # Write to file
        with open("frontend/static/frontend/data.json", "w") as json_file:
            json.dump(data_array, json_file, sort_keys=True, indent=4)
            json_file.close()

        return data_array

class ManualWeatherData(models.Model):
    date = models.DateTimeField(default=now, blank=True)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
    class Meta:
        ordering = ['date']