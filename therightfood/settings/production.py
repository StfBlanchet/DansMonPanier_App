"""
Django prod settings 
for therightfood project
"""


from . import *


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['dansmonpanier.online']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PW'],
        'HOST': '',
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

CSRF_COOKIE_SECURE = True   

SESSION_COOKIE_SECURE = True    

X_FRAME_OPTIONS = 'DENY'

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True  

# SECURE_SSL_REDIRECT = True  # activate once SSL is set up
