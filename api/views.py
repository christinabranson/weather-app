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


def kitchensink(request):
    logger.debug("baseapp.views.home.kitchensink")
    data = WeatherData.get_kitchen_sink()
    logger.debug(data)
    return JsonResponse(data, safe=False)