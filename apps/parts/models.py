from django.db import models

from datetime import datetime

# Create your models here.

class Parts(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'名称')
    desc = models.CharField(max_length=50, verbose_name=u'描述')
    image = models.ImageField(max_length=150, upload_to='parts/image/%Y%m',default=u'parts/image/default.png', verbose_name=u'封面图')
    price = models.IntegerField(default=1, verbose_name=u'现价')
    reference_price = models.IntegerField(default=1, verbose_name=u'原价')
    category = models.IntegerField(
        choices=(
            (1,'后盖'),(2,'保护壳/套'),(3,'电池'),(4,'耳机'),(5,'数据线'),
            (6,'保护膜'),(7,'充电器'),(8,'移动电源'),(9,'无线传输'),(10,'自拍杆')
        ),
        default=1,
        verbose_name=u'类别')
    adaptation = models.IntegerField(
        choices=(
            (1, 'M6S'), (2, 'M7Plus'), (3, 'M6'), (4, 'M6Plus'), (5, 'M2017'),
            (6, 'W909'), (7, 'S9'), (8, 'F106'), (9, 'F5')
        ),
        default=1,
        verbose_name=u'适用机型')
    is_hot = models.BooleanField(default=False, verbose_name=u'是否热卖')
    is_active = models.BooleanField(default=False, verbose_name=u'是否在做活动')
    status = models.IntegerField(choices=((1,'有货'),(2,'无货')), default=1, verbose_name=u'是否有货')
    sale_nums = models.IntegerField(default=0, verbose_name=u'销售量')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'配件信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PartsImage(models.Model):
    parts = models.ForeignKey(Parts, verbose_name=u'配件')
    index = models.IntegerField(default=1, verbose_name=u'序号')
    image= models.ImageField(max_length=150, upload_to='parts/%Y%m', verbose_name=u'图片')
    category = models.IntegerField(
        choices=(
            (1,'配件图片'),(2,'功能特色')
        )
    )
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'配件图片'
        verbose_name_plural = verbose_name


class TypicalSpecification(models.Model):
    parts = models.ForeignKey(Parts, verbose_name=u'配件')
    name = models.CharField(max_length=10, verbose_name=u'参数名')
    content = models.CharField(max_length=50, verbose_name=u'参数内容')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'参数规格'
        verbose_name_plural = verbose_name
