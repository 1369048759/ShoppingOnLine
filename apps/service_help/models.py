from django.db import models
from DjangoUeditor.models import UEditorField

from datetime import datetime
# Create your models here.

class ServiceHelp(models.Model):
    name = models.CharField(max_length=20, default=u'', verbose_name=u'名称')
    service_type = models.IntegerField(
        choices=((1,'账号管理'),(2,'购物指南'),(3,'订单管理'),(4,'配送方式'),(5,'支付方式'),
                 (6,'售后服务'),(7,'相关说明'),(8,'联系我们'),
                 (9,'关于手机售后FAQ'),(10,'关于手机售前FAQ'),(11,'产品使用')),
        default=1, verbose_name=u'服务类型'
    )
    service_id = models.IntegerField(default=1, verbose_name=u'服务id')
    content = UEditorField(
        width=800, height=600, imagePath="service/ueditor/",
        filePath="service/ueditor/", verbose_name=u"文章内容"
    )
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'服务帮助'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ServiceUserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, default=u'', verbose_name=u'手机')
    question_type = models.IntegerField(choices=((1,'留言'),(2,'投诉'),(3,'建议')), default=1)
    detail = models.CharField(max_length=300, default=u'', verbose_name=u'问题描述')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class District(models.Model):
    district = models.CharField(max_length=20, default=u'', verbose_name=u'省份')

    class Meta:
        verbose_name = u'省份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.district


class City(models.Model):
    city = models.CharField(max_length=10, default=u'', verbose_name=u'城市')
    district = models.ForeignKey(District, verbose_name=u'省份')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city


class ExperienceStore(models.Model):
    shopname = models.CharField(max_length=50, verbose_name=u'店名')
    group = models.IntegerField(choices=((1,'东区'),(2,'南区'),(3,'西区'),(4,'北区')), default=1)
    district = models.ForeignKey(District, verbose_name=u'省份')
    city = models.ForeignKey(City, verbose_name=u'城市')
    shopAddress = models.CharField(max_length=100, verbose_name=u'地址')
    shopTel = models.CharField(max_length=11, verbose_name=u'联系电话')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'体验店'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shopname

    def get_store_image(self):
        return self.stopimage_set.all()


class StopImage(models.Model):
    store = models.ForeignKey(ExperienceStore, verbose_name=u'店铺')
    image = models.ImageField(max_length=150, upload_to='stopImage/%Y%m', default='stopImage/default.png', verbose_name=u'图片')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'店铺图片'
        verbose_name_plural = verbose_name


class ServiceNetworkStation(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    district = models.ForeignKey(District, verbose_name=u'省份')
    city = models.ForeignKey(City, verbose_name=u'城市')
    category = models.IntegerField(choices=((1,'特约服务站'),(2,'客服中心')), verbose_name=u'类别')
    address = models.CharField(max_length=100, verbose_name=u'地址')
    tel = models.CharField(max_length=20, verbose_name=u'服务电话')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'售后服务网点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BrokenScreenQuestion(models.Model):
    question = models.CharField(max_length=150, verbose_name=u'问题描述')
    content = models.CharField(max_length=200, verbose_name=u'问题解决')
    category = models.IntegerField(choices=((1,'碎屏服务'),(2,'上门维修')), default=1, verbose_name=u'类别')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'保障服务问题解答'
        verbose_name_plural = verbose_name



