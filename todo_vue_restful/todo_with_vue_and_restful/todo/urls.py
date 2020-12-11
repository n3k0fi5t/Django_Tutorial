from django.urls import re_path

from .views import PostsView

app_name = 'todo'

urlpatterns = [
    re_path(r'^$', PostsView.as_view(), name='list'),
]