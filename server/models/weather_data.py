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

        data_array = {}
        data_array["data"] = []

        startDays = 5
        endDays = 5

        tz = pytz.timezone('America/New_York')
        time_now = datetime.now(tz=tz).date()
        time_midnight = tz.localize(datetime.combine(time_now, time(0, 0)), is_dst=None)
        start = time_midnight - timedelta(days=startDays)
        end = time_midnight + timedelta(days=endDays)

        weather_data = WeatherData.objects.filter(date__gte=start).filter(date__lte=end)
        manually_weather_data = ManualWeatherData.objects.filter(date__gte=start).filter(date__lte=end)

        weather_data_agg = WeatherData.objects.filter(date__gte=start).filter(date__lte=end).aggregate(total_accumulation=Sum('precip_amount'))
        manual_weather_data_agg = ManualWeatherData.objects.filter(date__gte=start).filter(date__lte=end).aggregate(total_accumulation=Sum('precip_amount'))

        total_accumulation = 0
        if weather_data_agg is not None and weather_data_agg['total_accumulation'] is not None:
            total_accumulation = total_accumulation + float(weather_data_agg['total_accumulation'])
        if manual_weather_data_agg is not None and manual_weather_data_agg['total_accumulation'] is not None:
            total_accumulation = total_accumulation + float(manual_weather_data_agg['total_accumulation'])

        data_array["total_accumulation"] = math.ceil(total_accumulation)

        startDaysNeg = -1*startDays
        accumulation = 0
        for x in range(startDaysNeg, endDays):
            day = time_midnight + timedelta(days=x)

            data = {}

            data["label"] = datetime.strftime(day, "%A, %-d %B")
            data["date"] = day

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

            data["percent_rain"] = round(data["amount_rain"] / data_array["total_accumulation"] * 100, 2)
            data["percent_manual"] = round(data["amount_manual"] / data_array["total_accumulation"] * 100, 2)
            data["percent_accumulation"] = round(data["amount_accumulation"] / data_array["total_accumulation"] * 100, 2)
            data["percent_empty"] = round(100 - data["percent_rain"] - data["percent_manual"] - data["percent_accumulation"], 2)

            # change them to a string and add the percentages
            for variable in {"percent_rain", "percent_manual", "percent_accumulation", "percent_empty"}:
                data[variable] = str(data[variable]) + "%"

            data_array["data"].append(data)

        return data_array

class ManualWeatherData(models.Model):
    date = models.DateTimeField(default=now, blank=True)
    precip_amount = models.FloatField(default=0, blank=False, null=False)
    class Meta:
        ordering = ['date']