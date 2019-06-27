from django.contrib import admin

from .models import User as CustomUser
from .models import WeatherData
from .models import ManualWeatherData

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    search_fields = ["email", "first_name", "last_name"]
    list_per_page = 25
admin.site.register(CustomUser, UserAdmin)

class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ("datetime", "precip_amount")
    list_per_page = 25
admin.site.register(WeatherData, WeatherDataAdmin)

class ManualWeatherDataAdmin(admin.ModelAdmin):
    list_display = ("datetime", "precip_amount")
    list_per_page = 25
admin.site.register(ManualWeatherData, ManualWeatherDataAdmin)