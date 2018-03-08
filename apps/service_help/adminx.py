import  xadmin

from .models import ServiceHelp, ServiceUserAsk, ExperienceStore, StopImage, District, \
    City, ServiceNetworkStation, BrokenScreenQuestion


class ServiceHelpXadmin(object):
    list_display = ['name', 'service_type', 'service_id', 'add_times']
    search_fields = ['name']
    list_filter = ['service_type', 'service_id', 'add_times']
    style_fields = {'content':'ueditor'}
    list_per_page = 20
    show_detail_fields = ['name']
    list_editable = ['name', 'service_type']


class ServiceUserAskXadmin(object):
    list_display = ['name', 'mobile', 'question_type', 'detail', 'add_times']
    search_fields = ['question_type']
    list_filter = ['question_type', 'add_times']
    list_per_page = 20
    show_detail_fields = ['name']
    readonly_fields = ['name', 'mobile', 'question_type', 'detail', 'add_times']


class DistrictXadmin(object):
    list_display = ['district']
    list_editable = ['district']


class CityXadmin(object):
    list_display = ['city', 'district']
    search_fields = ['city', 'district']
    list_filter = ['city', 'district']
    list_editable = ['city', 'district']


class ExperienceStoreXadmin(object):
    list_display = ['shopname', 'group', 'district', 'city', 'shopAddress', 'shopTel', 'add_times']
    search_fields = ['shopname', 'group', 'district', 'city', 'shopTel']
    list_filter = ['group', 'district', 'city', 'add_times']
    list_per_page = 20
    show_detail_fields = ['shopname']
    list_editable = ['shopname', 'shopAddress', 'shopTel']


class StoreImageXadmin(object):
    list_display = ['store','add_times']
    search_fields = ['store']
    list_per_page = 20
    show_detail_fields = ['name']

class ServiceNetworkStationXadmin(object):
    list_display = ['name', 'address', 'category', 'tel', 'district', 'city', 'add_times']
    search_fields = ['category', 'district', 'city']
    list_filter = ['category', 'district', 'city', 'add_times']
    list_per_page = 20
    show_detail_fields = ['name']
    list_editable = ['name', 'address', 'category', 'tel']


class BrokenScreenQuestionXadmin(object):
    list_display = ['question', 'content', 'add_times']
    list_filter = ['add_times']
    list_per_page = 20
    show_detail_fields = ['question']
    list_editable = ['question', 'content']

xadmin.site.register(ServiceHelp, ServiceHelpXadmin)
xadmin.site.register(ServiceUserAsk, ServiceUserAskXadmin)
xadmin.site.register(ExperienceStore, ExperienceStoreXadmin)
xadmin.site.register(StopImage, StoreImageXadmin)
xadmin.site.register(District, DistrictXadmin)
xadmin.site.register(City, CityXadmin)
xadmin.site.register(ServiceNetworkStation, ServiceNetworkStationXadmin)
xadmin.site.register(BrokenScreenQuestion, BrokenScreenQuestionXadmin)

