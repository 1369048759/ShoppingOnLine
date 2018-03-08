# -*- coding: UTF-8 -*-
# Author:Xiao Di

from .models import  Parts, PartsImage, TypicalSpecification
import  xadmin

class PartsImageInline(object):
    model = PartsImage
    extra = 0

class TypicalSpecificationInline(object):
    model = TypicalSpecification
    extra = 0

class PartsXadmin(object):
    list_display = [
        'name', 'desc', 'price', 'category',
        'adaptation', 'sale_nums', 'is_hot', 'is_active', 'add_times']
    search_fields = ['name', 'desc', 'category', 'adaptation']
    list_filter = ['price', 'category', 'adaptation', 'sale_nums', 'is_hot', 'is_active']
    list_per_page = 20
    show_detail_fields = ['name']
    list_editable = ['name', 'desc', 'price', 'category','adaptation' 'is_hot', 'is_active']
    readonly_fields = ['sale_nums']
    inlines = [PartsImageInline, TypicalSpecificationInline]


class PartsImageXadmin(object):
    list_display = ['parts', 'category', 'add_times']
    search_fields = ['parts', 'category']
    list_filter = ['parts', 'category', 'add_times']
    list_per_page = 20
    show_detail_fields = ['parts']
    list_editable = ['parts', 'category']


class TypicalSpecificationXadmin(object):
    list_display = ['parts', 'name', 'content', 'add_times']
    search_fields = ['parts', 'name']
    list_filter = ['parts', 'name', 'add_times']
    list_per_page = 20
    show_detail_fields = ['parts']
    list_editable = ['parts', 'name', 'content']


xadmin.site.register(Parts, PartsXadmin)
xadmin.site.register(PartsImage, PartsImageXadmin)
xadmin.site.register(TypicalSpecification, TypicalSpecificationXadmin)