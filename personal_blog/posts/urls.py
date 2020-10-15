from django.urls import re_path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostDeleteView,
    PostUpdateView,
)

APP_NAME = 'posts'

urlpatterns = [
    re_path(r'^list/$', PostListView.as_view(), name='list'),
    re_path(r'^create/$', PostCreateView.as_view(), name='create'),
    re_path(r'^(?P<id>\d+)/edit/$', PostUpdateView.as_view(), name='edit'),
    re_path(r'^(?P<id>\d+)/delete/$', PostDeleteView.as_view(), name='delete'),
    re_path(r'^(?P<id>\d+)/$', PostDetailView.as_view(), name='detail'),
]