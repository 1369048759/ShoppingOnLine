"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

import  xadmin

from .settings import MEDIA_ROOT
from users.views import IndexView
from users.views import permission_denied, page_not_found, page_error

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root' : MEDIA_ROOT}),
    url(r'^service/', include('service_help.urls', namespace='service')),
    url(r'^parts/', include('parts.urls', namespace='parts')),
    url(r'^carts/', include('carts.urls', namespace='carts')),
    url(r'^mobiles/', include('mobiles.urls', namespace='mobiles')),
    url(r'^download/', include('downloadcenter.urls', namespace='download')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^$', IndexView.as_view(), name='index')

]


