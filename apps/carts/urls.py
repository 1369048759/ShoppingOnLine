# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import  url
from .views import CartsAddView, CartsModifyView, CartsDelView, CartsCheckoutView
from .views import CartsInvoiceCheckView, CartsPlaymentView
urlpatterns = [
    url(r'^add/$', CartsAddView.as_view(), name='add'),
    url(r'^modify/$', CartsModifyView.as_view(), name='modify'),
    url(r'^del/(?P<product_name>.*)$', CartsDelView.as_view(), name='del'),
    url(r'^checkout/$', CartsCheckoutView.as_view(), name='checkout'),
    url(r'^invoice/$', CartsInvoiceCheckView.as_view(), name='invoice'),
    url(r'^playment/$', CartsPlaymentView.as_view(), name='playment'),
]