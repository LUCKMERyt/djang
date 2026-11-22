"""
WSGI config for Al_Ven project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Al_Ven.settings')

application = get_wsgi_application()

if not settings.DEBUG:
    application = WhiteNoise(
        application,
        root=str(settings.MEDIA_ROOT),
        prefix=settings.MEDIA_URL.lstrip('/'),
        max_age=0,
    )
    application = WhiteNoise(
        application,
        root=str(settings.STATIC_ROOT),
        prefix=settings.STATIC_URL.lstrip('/'),
    )
