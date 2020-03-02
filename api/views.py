from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
import logging
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import json
from django.http import JsonResponse
from server.models import WeatherData

logger = logging.getLogger(__name__)

def future_weather(request):
    logger.debug("api.views.home.future_weather")
    data = WeatherData.future_weather()
    logger.debug(data)
    return JsonResponse(data, safe=False)

def kitchensink(request):
    logger.debug("api.views.home.kitchensink")
    data = WeatherData.get_kitchen_sink()
    logger.debug(data)
    return JsonResponse(data, safe=False)

def at_a_glance(request):
    logger.debug("api.views.home.at_a_glance")
    data = WeatherData.get_at_a_glance()
    logger.debug(data)
    return JsonResponse(data, safe=False)