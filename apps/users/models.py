from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name=u'昵称')
    gender = models.IntegerField(
        choices=(
            (1, '保密'),(2, '男'),(3, '女')
        ), default=1, verbose_name=u'性别'
    )
    birday = models.DateTimeField(default=datetime.now, verbose_name=u'生日')
    mobile = models.CharField(max_length=11, default='', verbose_name=u'手机号')
    fixed_number = models.CharField(max_length=11, default='', verbose_name=u'固定号码')
    address = models.CharField(max_length=150, default=u'', verbose_name=u'居住地址')
    province = models.CharField(max_length=20, default=u'', verbose_name=u'省份')
    city= models.CharField(max_length=20, default=u'', verbose_name=u'城市')
    town = models.CharField(max_length=20, default=u'', verbose_name=u'区县')

    class Meta:
        verbose_name = u'个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=100, verbose_name=u'验证码')
    email = models.CharField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, verbose_name=u'发送类型')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class UserAddress(models.Model):
        user = models.ForeignKey(UserProfile, verbose_name=u'用户')
        consignee = models.CharField(max_length=50, default=u'', verbose_name=u'收件人')
        mobile = models.CharField(max_length=11, default=u'', verbose_name=u'联系电话')
        province = models.CharField(max_length=20, default=u'', verbose_name=u'省份')
        city = models.CharField(max_length=20, default=u'', verbose_name=u'城市')
        town = models.CharField(max_length=20, default=u'', verbose_name=u'区')
        address = models.CharField(max_length=200, default=u'', verbose_name=u'地址')

        class Meta:
            verbose_name = u'收获地址'
            verbose_name_plural = verbose_name

        def __str__(self):
            return self.name


class UserOrder(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    cart = models.CharField(max_length=100000, verbose_name=u'购物车')
    price = models.IntegerField(default=0, verbose_name=u'总价')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    class Meta:
        verbose_name = u'用户订单'
        verbose_name_plural =verbose_name

