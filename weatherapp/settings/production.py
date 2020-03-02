from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

if DEBUG:
    STATIC_URL = '/waterstatic/'
else:
    STATIC_URL = '/static/'