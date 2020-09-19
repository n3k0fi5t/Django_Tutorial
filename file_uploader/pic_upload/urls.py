from django.urls import re_path, include
from .views import PicDetail, PicList, PicUpload
from .views import PictureUpload, PictureList, PictureDetail

app_name = 'pic_upload'

urlpatterns = [
    re_path(r'^$', PictureList.as_view(), name='pic_list'),
    re_path(r'^pic/upload/$', PictureUpload.as_view(), name='pic_upload'),
    re_path(r'^pic/(?P<id>\d+)/$', PictureDetail.as_view(), name='pic_detail'),
]