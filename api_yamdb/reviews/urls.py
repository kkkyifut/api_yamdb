from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:titles>/', views.titles, name='titles'),
    path('<str:titles>/<int:title_id>/<int:reviews_id>/',
         views.review_view, name='review'),
    path('<str:titles>/<int:title_id>/<int:review_id>/edit/',
         views.review_edit, name="edit"),
]
