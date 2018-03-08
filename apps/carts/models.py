from django.db import models

from datetime import  datetime

from users.models import UserProfile

# Create your models here.

class CartsInfo(models.Model):
    product_id = models.IntegerField(default=1, verbose_name=u'商品ID')
    name = models.CharField(max_length=50, verbose_name=u'商品名称')
    image = models.CharField(max_length=150, verbose_name=u'图片')
    price = models.IntegerField(default=1, verbose_name=u'单价')
    quantity = models.IntegerField(default=1, verbose_name=u'数量')
    total_price = models.IntegerField(default=1, verbose_name=u'小计')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


class CartsForUser(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    cart = models.CharField(max_length=100000, verbose_name=u'购物车')
    price = models.IntegerField(default=0, verbose_name=u'总价')
    status = models.IntegerField(
        choices=(
            (0, '未结算'),
            (1, '已结算')
        ), default=0, verbose_name=u'是否结算'
    )

    class Meta:
        verbose_name = u'用户购物车'
        verbose_name_plural = verbose_name


class RecentlyView(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    product_id = models.IntegerField(default=1, verbose_name=u'商品ID')
    product_type = models.IntegerField(
        choices=(
            (1,'手机'),(2,'配件')
        ), default=1, verbose_name=u'商品类型'
    )
    add_times = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u'访问时间')

    class Meta:
        verbose_name = u'最近浏览'
        verbose_name_plural = verbose_name


class ElectronicInvoice(models.Model):
    invoice_title = models.IntegerField(
        choices=(
            (1,'个人'),(2,'单位')
        ), default=1, verbose_name=u'发票抬头'
    )
    inv_payee = models.CharField(max_length=50, default=u'', verbose_name=u'姓名')
    inv_phone = models.CharField(max_length=11, default=u'', verbose_name=u'联系方式')
    inv_taxno = models.CharField(max_length=18, default=u'', verbose_name=u'身份证号')
    inv_email =  models.CharField(max_length=50, default=u'', verbose_name=u'邮箱')
    order_number = models.CharField(max_length=25, default=u'', verbose_name=u'订单号')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'电子发票'
        verbose_name_plural = verbose_name


class CartsOrder(models.Model):
    order_number = models.CharField(max_length=50, verbose_name=u'订单编号')
    is_playment = models.IntegerField(
        choices=(
            (1, '未支付'),
            (2, '已支付'),
            (3, '已取消')
        ), default=1, verbose_name=u'订单是否支付'
    )
    order_times = models.DateTimeField(default=datetime.now, verbose_name=u'下单时间')
    order_price = models.IntegerField(default=0, verbose_name=u'订单金额')
    address = models.CharField(max_length=200, verbose_name=u'收货地址')
    playment_type = models.IntegerField(
        choices=(
            (1, '在线支付'),(2, '货到付款')
        ), default=1, verbose_name=u'支付方式'
    )
    delivery_type = models.IntegerField(
        choices=(
            (1, '顺丰速运'),
        ), default=1, verbose_name=u'配送方式'
    )
    carts = models.CharField(max_length=1000000, verbose_name=u'商品清单')
    payment_bank = models.CharField(max_length=20, default=u'', verbose_name=u'支付银行')
    user_id = models.IntegerField(default=0, verbose_name=u'用户')

    class Meta:
        verbose_name = u'用户订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_number


class PaymentBank(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'名称')
    nick_name = models.CharField(max_length=50, verbose_name=u'别名')
    image = models.ImageField(max_length=150, upload_to='paymentbank/%Y%m', verbose_name=u'图片')
    category = models.IntegerField(
        choices=(
            (1, '第三方平台支付'),
            (2, '快捷支付'),
            (3, '银行网银')
        )
    )

    class Meta:
        verbose_name = u'支付方式'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name










