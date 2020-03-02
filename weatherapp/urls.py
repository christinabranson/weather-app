"""weatherapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views as api_views
from django.conf import settings

urlpatterns = [
    path('api/future_weather', api_views.future_weather, name='api.future_weather'),
    path('api/kitchensink', api_views.kitchensink, name='api.kitchensink'),
    path('api/at_a_glance', api_views.at_a_glance, name='api.at_a_glance'),
    path('', include('frontend.urls')),
    path('react/', include('frontend_react.urls')),
    path('admin/', admin.site.urls),
]

# we only need the front end code on the development
if settings.DEBUG:
    urlpatterns.append(path('', frontend_views.index, name='index'))