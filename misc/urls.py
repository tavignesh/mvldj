from django.contrib import admin
from django.urls import path, include
from misc.views import err404, unknown_error

urlpatterns = [
    path('unknownerr', unknown_error, name='unknown_error'),
    path('', err404, name='err404'),
]