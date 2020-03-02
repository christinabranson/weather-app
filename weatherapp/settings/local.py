from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

if DEBUG:
    STATIC_URL = '/waterstatic/'
else:
    STATIC_URL = '/static/'