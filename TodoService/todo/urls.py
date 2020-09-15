from django.urls import path, re_path
from .views import TodoView, delete_todo_item, cross_off_item

app_name = 'todo'

urlpatterns = [
    re_path(r'^$', TodoView.as_view(), name='list'),
    re_path(r'^delete/(?P<todo_id>[0-9]+)/$', delete_todo_item, name='delete'),
    re_path(r'^cut/(?P<todo_id>[0-9]+)/$', cross_off_item, name='cut'),
]