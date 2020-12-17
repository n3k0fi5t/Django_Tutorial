from django.urls import re_path

from .views import (
    TodoItemListAPIView,
    TodoItemAPIView,
)

app_name = 'todo'

urlpatterns = [
    re_path(r'^items/?$', TodoItemListAPIView.as_view(), name='todo_list_api'),
    re_path(r'^items/(?P<id>\d+)$', TodoItemAPIView.as_view(), name='todo_api'),
]