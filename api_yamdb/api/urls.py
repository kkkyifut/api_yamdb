from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIUserSignup, APIUserGetToken, UserViewSet, ReviewViewSet,
                    CommentViewSet, TitleViewSet, CategoryViewSet,
                    GenreViewSet, UserMeViewSet)

app_name = 'api-v1'

user_me_detail = UserMeViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})

router_v1 = SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/users/me/', user_me_detail, name='user-me-detail'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APIUserSignup.as_view()),
    path('v1/auth/token/', APIUserGetToken.as_view()),
]
