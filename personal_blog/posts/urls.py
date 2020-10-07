from django.urls import re_path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostDeleteView,
    PostUpdateView
)

APP_NAME = 'posts'

urlpatterns = [
    re_path(r'^list/$', PostListView.as_view()),
    re_path(r'^detail/$', PostDetailView.as_view()),
    re_path(r'^create/$', PostCreateView.as_view()),
    re_path(r'^update/$', PostDeleteView.as_view()),
    re_path(r'^delete$', PostUpdateView.as_view()),
]