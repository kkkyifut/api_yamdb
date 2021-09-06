from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
]
