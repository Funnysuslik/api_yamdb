from django.urls import path

from .views import ReviewsViewSet, CommentsViewSet


review_list = ReviewsViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

review_detail = ReviewsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

comment_list = CommentsViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

comment_detail = CommentsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('v1/titles/<int:title_id>/reviews/', review_list, name='review-list'),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/', review_detail, name='review-detail'),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/comments', comment_list, name='comment-list'),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/comments/<int:comment_id>', comment_detail, name='comment-detail'),
]