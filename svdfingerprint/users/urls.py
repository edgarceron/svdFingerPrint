"""Urls for users app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('check_fingerprint', views.check_fingerprint, name='check_fingerprint'),
    path('upload/', webservices.ImageViewSet.as_view(), name='upload'),
]