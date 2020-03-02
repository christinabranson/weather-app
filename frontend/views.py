import logging
from django.shortcuts import get_object_or_404, render
from server.models import WeatherData

logger = logging.getLogger(__name__)

def index(request):
    logger.debug("frontend.views.index")

    at_a_glance_data = WeatherData.get_at_a_glance()

    return render(request, 'frontend/index.html', {
        'at_a_glance_data': at_a_glance_data
    })