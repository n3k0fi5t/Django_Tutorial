from django.urls import re_path
from .views import UserRegistration, UserLoginView, UserLogoutView

app_name = 'registration'

urlpatterns = [
    re_path(r'^$', UserRegistration.as_view(), name='register'),
    re_path(r'^login/$', UserLoginView.as_view(), name='login'),
    re_path(r'^logout/$', UserLogoutView.as_view(), name='logout'),
]