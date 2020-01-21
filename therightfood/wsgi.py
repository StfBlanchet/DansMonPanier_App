"""
WSGI config for
therightfood project.
"""


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therightfood.settings')

application = get_wsgi_application()
