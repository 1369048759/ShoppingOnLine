# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import MobileListView, MobileInfoView

urlpatterns = [
    url(r'^list/$', MobileListView.as_view(), name='list'),
    url(r'^info/(?P<mobile_id>.*)$', MobileInfoView.as_view(), name='info')
]