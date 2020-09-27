from django.urls import re_path
from .views import TaskBoard, TaskSubmit

app_name = 'crawler'

urlpatterns = [
    re_path(r'^status/$', TaskBoard.as_view(), name='status'),
    re_path(r'^submit/$', TaskSubmit.as_view(), name='submit'),
]