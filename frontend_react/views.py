from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
import logging
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import json
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def index(request):
    logger.debug("frontend.views.index")

    return render(request, 'index.html', {

    })