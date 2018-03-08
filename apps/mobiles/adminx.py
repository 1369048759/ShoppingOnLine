# -*- coding: UTF-8 -*-
# Author:Xiao Di

import xadmin

from .models import Mobile, MobileImage, TypicalSpecification

class MobileImageInline(object):
    model = MobileImage
    extra = 0

class TypicalSpecificationInline(object):
    model = TypicalSpecification
    extra = 0

class MobileXadmin(object):
    list_display = ['name', 'desc', 'price','original_price','sale_nums','add_times']
    search_fields = ['name', 'desc','price','original_price','sale_nums']
    list_filter = ['price','original_price','sale_nums', 'add_times']
    list_per_page = 20
    show_detail_fields = ['name']
    list_editable = ['name', 'desc', 'price', 'original_price']
    readonly_fields = ['sale_nums']
    inlines = [MobileImageInline, TypicalSpecificationInline]


class MobileImageXadmin(object):
    list_display = ['mobile', 'index' ,'image', 'category', 'add_time']
    search_fields = ['mobile', 'category']
    list_filter = ['mobile', 'category', 'add_time']
    list_per_page = 20
    show_detail_fields = ['mobile']
    list_editable = ['mobile',  'image', 'category']




class TypicalSpecificationXadmin(object):
    list_display = ['mobile','os', 'cpu', 'memory', 'memory_space', 'screen_size', 'resolution', 'rear_facing_camera', 'facing_camera', 'battery_capacity', 'time_to_market']
    search_fields = ['os']
    list_filter = ['os', 'time_to_market']
    list_per_page = 20
    show_detail_fields = ['mobile']
    list_editable = ['mobile', 'os', 'cpu', 'memory', 'memory_space', 'screen_size', 'resolution','rear_facing_camera', 'facing_camera', 'battery_capacity']


xadmin.site.register(Mobile, MobileXadmin)
xadmin.site.register(MobileImage, MobileImageXadmin)
xadmin.site.register(TypicalSpecification, TypicalSpecificationXadmin)
