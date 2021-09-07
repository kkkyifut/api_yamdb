from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<str:title>/', views.title_view, name='title'),
    path('<str:title>/<int:reviews_id>/', views.review_view, name='review'),
    path("<str:title>/<int:review_id>/edit/", views.review_edit, name="edit"),
]
