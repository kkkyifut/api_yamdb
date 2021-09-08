from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIUserSignup, APIUserGetToken, UserViewSet, ReviewViewSet,
                    CommentViewSet)

app_name = 'api-v1'

router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APIUserSignup.as_view()),
    path('v1/auth/token/', APIUserGetToken.as_view()),
]
