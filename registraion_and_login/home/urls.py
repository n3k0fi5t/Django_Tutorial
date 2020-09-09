from django.urls import re_path
from .views import Home

app_name = 'home'

urlpatterns = [
    re_path(r'^$', Home.as_view(), name='home'),
]