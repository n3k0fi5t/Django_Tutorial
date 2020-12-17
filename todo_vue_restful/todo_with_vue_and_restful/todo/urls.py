from django.urls import re_path

from .views import TodoItemAPIView

app_name = 'todo'

urlpatterns = [
    re_path(r'^items/$', TodoItemAPIView.as_view(), name='todo_api'),
]