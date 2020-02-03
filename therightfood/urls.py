"""
therightfood URL
Configuration
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('explore.urls')),
    # protect admin access by renaming url
    path('********/', admin.site.urls),
]
