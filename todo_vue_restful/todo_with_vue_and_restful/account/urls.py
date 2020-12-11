from django.urls import include, re_path

from .views import UserLoginAPIView

urlpatterns = [
    re_path(r'^login/$', UserLoginAPIView.as_view()),
]