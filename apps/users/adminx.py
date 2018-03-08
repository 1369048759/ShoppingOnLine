# -*- coding: UTF-8 -*-
# Author:Xiao Di

from xadmin import views
import xadmin

from .models import UserAddress


class UserAddressXadmin(object):
    list_display = ['user', 'consignee', 'mobile', 'province', 'city', 'town', 'address']
    search_fields = ['user', 'consignee', 'mobile', 'province', 'city', 'town', 'address']
    list_filter = ['province', 'city', 'town']
    refresh_times = [3,5]
    list_per_page = 20
    show_detail_fields = ['user']
    list_editable = ['user', 'consignee', 'mobile', 'address']

class GlobalSetting(object):
    menu_style = "accordion"
    # 设置base_site.html的Title
    site_title = '金立手机后台管理'
    # 设置base_site.html的Footer
    site_footer  = '金立手机后天管理系统'


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(UserAddress, UserAddressXadmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
