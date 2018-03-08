# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import DownLoadCenterView

urlpatterns = [
    url(r'^center/$', DownLoadCenterView.as_view(), name='center')
]