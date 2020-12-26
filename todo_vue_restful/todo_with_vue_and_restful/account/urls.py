from django.urls import include, re_path

from .views import (
    UserLoginAPIView,
    UserLogoutAPIView,
    UserProfileAPIView,
    UserRegisterAPIView,
    UsernameOrEmailCheck,
)

urlpatterns = [
    re_path(r'^login/$', UserLoginAPIView.as_view()),
    re_path(r'^logout/$', UserLogoutAPIView.as_view()),
    re_path(r'^profile/$', UserProfileAPIView.as_view()),
    re_path(r'^register/$', UserRegisterAPIView.as_view()),
    re_path(r'^check_username_or_email/$', UsernameOrEmailCheck.as_view()),
]