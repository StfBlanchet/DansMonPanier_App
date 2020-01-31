"""
therightfood URL
Configuration
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('explore.urls')),
    # protect admin access by renaming url
    path('eFv$951@Pl!*/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
