from django.urls import include, path

from .views import APIUserSignup


urlpatterns = [
    path('v1/auth/signup/', APIUserSignup.as_view()),
]