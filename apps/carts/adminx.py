import xadmin

from .models import PaymentBank, CartsForUser, RecentlyView,ElectronicInvoice, CartsOrder

class PaymentBankXadmin(object):

    list_display = ['name','nick_name','image','category']
    search_fields = ['name','nick_name','image','category']
    list_filter = ['name','nick_name','image','category']
    list_per_page = 20
    show_detail_fields = ['name']
    list_editable = ['name', 'nick_name', 'image', 'category']


class CartsForUserXadmin(object):
    list_display = ['user', 'cart', 'price', 'status']
    search_fields = ['user', 'price', 'status']
    list_filter = ['price', 'status']
    list_per_page = 20
    show_detail_fields = ['user']
    readonly_fields = ['user', 'cart', 'price', 'status']


class RecentlyViewXadmin(object):
    list_display = ['user', 'product_id', 'product_type', 'add_times']
    search_fields = ['user', 'product_id', 'product_type']
    list_filter = ['user', 'product_id', 'product_type', 'add_times']
    list_per_page = 20
    show_detail_fields = ['user']
    readonly_fields = ['user', 'product_id', 'product_type', 'add_times']


class ElectronicInvoiceXadmin(object):
    list_display = ['inv_payee', 'invoice_title', 'inv_phone', 'inv_taxno', 'inv_email', 'order_number', 'add_times']
    search_fields = ['inv_payee', 'invoice_title', 'inv_phone', 'inv_taxno', 'inv_email', 'order_number']
    list_filter = ['inv_payee', 'invoice_title', 'inv_phone', 'inv_taxno', 'inv_email', 'order_number', 'add_times']
    list_per_page = 20
    show_detail_fields = ['inv_payee']
    readonly_fields = ['inv_payee', 'invoice_title', 'inv_phone', 'inv_taxno', 'inv_email', 'order_number', 'add_times']


class CartsOrderXadmin(object):
    list_display = ['order_number', 'is_playment', 'order_times', 'order_price', 'address', 'playment_type', 'delivery_type', 'payment_bank', 'user_id', 'carts']
    search_fields = ['order_number', 'is_playment', 'order_times', 'order_price', 'address', 'playment_type', 'delivery_type', 'payment_bank', 'user_id']
    list_filter = ['order_number', 'is_playment', 'order_times', 'order_price', 'address', 'playment_type', 'delivery_type', 'payment_bank', 'user_id']
    list_per_page = 20
    show_detail_fields = ['order_number']
    readonly_fields = ['order_number', 'is_playment', 'order_times', 'order_price', 'address', 'playment_type', 'delivery_type', 'payment_bank', 'user_id', 'carts']

xadmin.site.register(PaymentBank, PaymentBankXadmin)
xadmin.site.register(CartsForUser, CartsForUserXadmin)
xadmin.site.register(RecentlyView, RecentlyViewXadmin)
xadmin.site.register(ElectronicInvoice, ElectronicInvoiceXadmin)
xadmin.site.register(CartsOrder, CartsOrderXadmin)