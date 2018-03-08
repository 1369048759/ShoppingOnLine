from django.db import models

from datetime import datetime

# Create your models here.


class Mobile(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'手机名称')
    image = models.ImageField(max_length=150, upload_to='mobile/image/%Y%m', verbose_name=u'手机图片')
    desc = models.CharField(max_length=500, verbose_name=u'描述')
    price = models.IntegerField(default=1, verbose_name=u'现价')
    original_price = models.IntegerField(default=1, verbose_name=u'原价')
    category = models.IntegerField(
        choices=(
            (1,'智能手机'),(2,'功能手机')
        )
    )
    appearance = models.IntegerField(
        choices=(
            (1,'触屏'),(2,'翻盖')
        )
    )
    series = models.IntegerField(
        choices=(
            (1,'M系列'),(2,'S系列'),(3,'天鉴系列'),(4,'F系列'),(5,'金钢系列'),(6,'其他机型')
        )
    )
    sale_nums = models.IntegerField(default=0, verbose_name=u'销售量')
    add_times = models.DateTimeField(default=datetime.now, verbose_name=u'上市时间')
    status = models.IntegerField(
        choices=(
            (1,'无'),(2,'新品'),(3,'首发'),(4,'热卖')
        )
    )
    is_onsale = models.IntegerField(
        choices=(
            (1, '有货'),(2, '缺货')
        ), default=1, verbose_name=u'是否有货'
    )

    class Meta:
        verbose_name = u'手机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MobileImage(models.Model):
    mobile = models.ForeignKey(Mobile, verbose_name=u'手机')
    index = models.IntegerField(default=1, verbose_name=u'序号')
    category= models.IntegerField(
        choices=(
            (1,'配件图片'),(2,'功能特色')
        )
    )
    image = models.ImageField(max_length=150, upload_to='mobile/mobile_image/%Y%m', verbose_name=u'手机图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'手机图片'
        verbose_name_plural = verbose_name


class TypicalSpecification(models.Model):
    mobile = models.ForeignKey(Mobile, verbose_name=u'手机')
    time_to_market = models.DateTimeField(default=datetime.now, verbose_name=u'上市时间')
    os = models.IntegerField(
        choices=(
            (1, 'amigo3.0(Android5.0)'),
            (2, 'amigo3.1(Android5.1)'),
            (3, 'amigo3.2(Android6.0)'),
            (4, 'amigo3.5(Android5.1)'),
            (5, 'amigo3.5(Android6.0)'),
            (6, 'amigo4.0(Android7.0)'),
            (7, 'amigo5.0(Android7.1)'),
            (8, '天鉴os')
        ),default=1, verbose_name=u'操作系统'
    )
    cpu = models.IntegerField(
        choices=(
            (1, 'HelioP25'),
            (2, 'MSM8916'),
            (3, 'MSM8920'),
            (4, 'MSM8940'),
            (5, 'MT6582'),
            (6, 'MT6732'),
            (7, 'MT6735'),
            (8, 'MT6737'),
            (9, 'MT6750'),
            (10, 'MT6755'),
            (11, 'MT6582')
        ),default=1, verbose_name=u'cpu型号'
    )

    memory = models.IntegerField(
        choices=(
            (1, '1GB'),
            (2, '2GB'),
            (3, '3GB'),
            (4, '4GB'),
            (5, '6GB')
        ),default=1, verbose_name=u'内存'
    )

    memory_space = models.IntegerField(
        choices = (
            (1, '8GB'),
            (2, '16GB'),
            (3, '32GB'),
            (4, '64GB'),
            (5, '256GB'),
        ),default=1, verbose_name=u'存储空间'
    )


    memory_expansion_space = models.IntegerField(
        choices=(
            (1, '128GB'),
            (2, '256GB')
        ),default=1, verbose_name=u'存储拓展容量'
    )

    network_band = models.IntegerField(
        choices=(
            (1, 'GSM：B2/B3/B5/B8；TD_SCDMA：B34/B39；TDD_LTE：B38/B39/B40//B41/B34；WCDMA：B1/B2/B5/B8；FDD-LTE：B1/B3/B5/B8/B7；CDMA1X&EVDO；BC0'),
        ),default=1, verbose_name=u'网络频段'
    )

    SIM = models.IntegerField(
        choices=(
            (1, '双nano SIM卡'),
        ),default=1, verbose_name=u'SIM卡尺寸'
    )

    appearance = models.IntegerField(
        choices=(
            (1, '触屏'),
            (2, '翻盖')
        ),default=1, verbose_name=u'外形'
    )

    appearance_of_size = models.IntegerField(
        choices=(
            (1, '161x81x8mm'),(2, '163x81x8mm'),
            (3,'150x75x8mm'),(4,'152x75x7mm'),(5,'154x76x7mm'),(6,'154x75x7mm'),
            (7,'155x77x7mm'),(8,'155x77x9mm'),(9,'155x77x10mm'),(10,'157x76x7mm'),
            (11,'140x71x9mm'),(12,'143x70x8mm'),(13,'144x71x10mm'),(14,'145x70x9mm'),(15,'148x73x8mm'),(16,'149x74x8mm'),
            (17,'133x66x12mm'),(18,'134x67x8mm'),(19,'137x67x8mm'),
            (20, '121x63x16mm'),(21, '124x63x16mm'),
            (22, '113x58x18mm'),(23, '116x60x19mm')
        ),default=1, verbose_name=u'外观尺寸'
    )

    weight = models.IntegerField(
        choices=(
            (1, '130g'),(2, '135g'),
            (3, '140g'),(4, '145g'),
            (5, '150g'),(6, '155g'),
            (7, '160g'),(8, '165g'),
            (9, '170g'),(10, '175g'),
            (11, '180g'),(12, '185g'),
            (12, '190g'),(13, '195g'),
            (14, '200g'),(15, '205g'), (16, '210g')
        ),default=1, verbose_name=u'重量'
    )

    fuselage_material = models.IntegerField(
        choices=(
            (1, '金属'),
            (2, '塑料+金属'),
            (4,'金属+皮革'),
            (5,'合金镁铝')
        ),default=1, verbose_name=u'机身材质'
    )

    screen_size = models.IntegerField(
        choices=(
            (1, '4.0英寸'),(2, '4.2英寸'),(3, '4.5英寸'),
            (4, '5.0英寸'),(5, '5.2英寸'),(6, '5.3英寸'),(7, '5.5英寸'),
            (8, '5.7英寸'),(9, '6.0英寸')
        ),default=1, verbose_name=u'屏幕尺寸'
    )

    resolution = models.IntegerField(
        choices=(
            (1, '2560x1440'),(2, '2160x1080'),(3, '1920x1080'),(4, '1280x720'),
            (5, '1440x720'),(6, '854x480'),(7, '800x480')
        ),default=1, verbose_name=u'分辨率'
    )

    PPI = models.IntegerField(
        choices=(
            (1, '235'), (2, '268'), (3, '277'), (4, '293'), (5, '368'), (6, '400')
        ),default=1, verbose_name=u'PPI'
    )

    screen_color = models.IntegerField(
        choices=(
            (1, '1600W色'),
        ),default=1, verbose_name=u'屏幕色彩'
    )

    screen_type = models.IntegerField(
        choices=(
            (1, '电容触摸屏'),
            (2, '电容触摸屏+多点触控')
        ),default=1, verbose_name=u'屏幕类型'
    )

    screen_material = models.IntegerField(
        choices=(
            (1, 'IPS'),
            (2, 'AMOLED'),
            (3, 'TFT')
        ),default=1, verbose_name=u'屏幕材质'
    )

    rear_facing_camera = models.IntegerField(
        choices=(
            (1,'1200W+1300W'),(2,'1300W+500W'),(3,'1600W+800W'),(4,'800W'),(5,'1200W'),(6,'1300W'),
        ),default=1, verbose_name=u'后置摄像头'
    )

    facing_camera = models.IntegerField(
        choices=(
            (1, '2000W+800W'),(2,'1600W'),(3,'1300W'),(4,'800W'),(5, '500W')
        ),default=1, verbose_name=u'后置摄像头'
    )

    sensor = models.IntegerField(
        choices=(
            (1, 'CMOS'),
        ),default=1, verbose_name=u'传感器'
    )

    flashlight = models.IntegerField(
        choices=(
            (1, 'LED补光灯'),
            (2, '双色温闪光灯')
        ),default=1, verbose_name=u'闪光灯'
    )

    focusing_mode = models.IntegerField(
        choices=(
            (1, '自动对焦/数码变焦'),
            (2, '全像素双核对焦')
        ), default=1, verbose_name=u'对焦模式'
    )

    video_shooting = models.IntegerField(
        choices=(
            (1, '1080P/720P/480P/QCIF'),(2, '4K/720P/480P/QCIF'),(3, '720P/480P/QCIF')
        ),default=1, verbose_name=u'视频拍摄'
    )

    music_play = models.IntegerField(
        choices=(
            (1, '支持'),(2, '不支持')
        ),default=1, verbose_name=u'音乐播放'
    )

    video_play = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'视频播放'
    )

    image_play = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'图片播放'
    )

    radio = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'收音机'
    )

    recorder = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'录音机'
    )

    recorder_call = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'通话录音'
    )

    battery_capacity = models.IntegerField(
        default=2000, verbose_name=u'电池容量'
    )

    battery_type = models.IntegerField(
        choices=(
            (1, '聚合物锂离电池'),
        ),default=1, verbose_name=u'电池类型'
    )

    bluetooth = models.IntegerField(
        choices=(
            (1, '蓝牙4.0'),
            (2, '蓝牙4.1'),
            (3, '蓝牙4.2')
        ),default=1, verbose_name=u'蓝牙'
    )

    interface = models.IntegerField(
        choices=(
            (1, 'Micro-USB2.0'),(2, 'Micro 5pin'),(3, 'USB2.0/Type-C')
        ),default=1, verbose_name=u'接口'
    )

    headphone_jack = models.IntegerField(
        choices=(
            (1, '3.5mm'),(2, 'Type-C'),(3, '无')
        ),default=1, verbose_name=u'耳机接口'
    )

    wifi = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ),default=1, verbose_name='WIFI'
    )

    GPS = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ),default=1, verbose_name=u'GPS导航'
    )

    keyboard_type = models.IntegerField(
        choices=(
            (1, '虚拟键盘'),(2, '实体键盘'),(3, '虚拟键盘+实体键盘')
        ),default=1, verbose_name=u'键盘类型'
    )

    input_mode = models.IntegerField(
        choices=(
            (1, '触控'),(2, '触控+指纹识别'),(3,'触控+实体键盘')
        ),default=1, verbose_name=u'输入方式'
    )

    gyroscope = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'陀螺仪'
    )

    light_sensor = models.IntegerField(
        choices=(
            (1, '支持'),(2, '不支持')
        ),default=1, verbose_name=u'光线感应器'
    )

    accelerometer = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'重力感应'
    )

    distance = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'距离感应'
    )

    electronic_compass = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'电子罗盘'
    )

    compass = models.IntegerField(
        choices=(
            (1, '支持'), (2, '不支持')
        ), default=1, verbose_name=u'指南针'
    )

    class Meta:
        verbose_name = u'参数规格'
        verbose_name_plural = verbose_name

