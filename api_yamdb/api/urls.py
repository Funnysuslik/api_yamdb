from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import APISignUp, APIUser
from .views import CommentsViewSet, ReviewsViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', APIUser.as_view(), name='me'),

    path('v1/', include(router_v1.urls)),
]
