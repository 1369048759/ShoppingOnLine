# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import ServiceHelpDetailView, ServiceHelpListView, ServiceUserAskView, \
    ExperienceStoreView, ServiceNetworkStationView, ServiceBrokenScreenView, \
    ServiceIMEIView, ServiceHintView, ServiceOutsiteRepairView, ServiceEmptyView

urlpatterns = [
    url(r'^help/(?P<service_type>.*)/(?P<service_id>.*)$', ServiceHelpDetailView.as_view(), name='detail'),
    url(r'^list/$', ServiceHelpListView.as_view(), name='list'),
    url(r'^user/ask/$', ServiceUserAskView.as_view(), name='user/ask'),
    url(r'^experience/store/$', ExperienceStoreView.as_view(), name='experience/store'),
    url(r'^network/station/$', ServiceNetworkStationView.as_view(), name='network/station'),
    url(r'^broken/screen/$', ServiceBrokenScreenView.as_view(), name='broken/screen'),
    url(r'^IMEI/$', ServiceIMEIView.as_view(), name='IMEI'),
    url(r'^hint/$', ServiceHintView.as_view(), name='hint'),
    url(r'^outsite/repair/$', ServiceOutsiteRepairView.as_view(), name='outsite/repair'),
    url(r'^empty/$',ServiceEmptyView.as_view(), name='empty')
]