# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import UserLoginView, UserRegisterView, UserForgetPwdView,UserActiveView
from .views import ModifyPwdView, UserAddressCheckView,UserCenterMyOrderView, UserCenterMyOrderDetailView
from .views import UserCenterMyOrderCancelView, UserCenterCashView,UserCenterRecycleView
from .views import UserCenterAddressView,UserCenterAddressModifyView, UserCenterAddressDelView
from .views import UserCenterAddressNewView, UserCenterUserInfoView, LogoutView
urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^register/$', UserRegisterView.as_view(), name='register'),
    url(r'^forget/$', UserForgetPwdView.as_view(), name='forget'),
    url(r'^active/(?P<active_code>.*)$', UserActiveView.as_view(), name='active'),
    url(r'^modify/(?P<modify_code>.*)$', ModifyPwdView.as_view(), name='modify'),
    url(r'^address/$', UserAddressCheckView.as_view(), name='address'),
    url(r'^order_list/$', UserCenterMyOrderView.as_view(), name='order_list'),
    url(r'^order_detail/(?P<order_number>.*)$', UserCenterMyOrderDetailView.as_view(), name='order_detail'),
    url(r'^order_cancel/(?P<order_number>.*)$', UserCenterMyOrderCancelView.as_view(), name='order_cancel'),
    url(r'^cash/$', UserCenterCashView.as_view(), name='cash'),
    url(r'^recycle/$', UserCenterRecycleView.as_view(), name='recycle'),
    url(r'^user_address/$', UserCenterAddressView.as_view(), name='user_address'),
    url(r'^modify_address/$', UserCenterAddressModifyView.as_view(), name='modify_address'),
    url(r'^del_address/$', UserCenterAddressDelView.as_view(), name='del_address'),
    url(r'^new_address/$', UserCenterAddressNewView.as_view(), name='new_address'),
    url(r'^info/$', UserCenterUserInfoView.as_view(), name='info'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]