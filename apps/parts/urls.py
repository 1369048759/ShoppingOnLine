# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import PartsListView, PartsInfoView

urlpatterns = [
    url(r'^list/$', PartsListView.as_view(), name='list'),
    url(r'^info/(?P<parts_id>.*)$', PartsInfoView.as_view(), name='info')
]