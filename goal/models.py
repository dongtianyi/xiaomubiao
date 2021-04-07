from django.db import models

# Create your models here.
# from django.contrib.auth.models import User


class SetUp(models.Model):
    # user id, 一个用户可以有多个配置
    user_id = models.PositiveIntegerField()
    # 配置名字: 自己取一个名字
    name = models.CharField(max_length=30)
    # 每周完成几次
    times = models.PositiveIntegerField(default=3)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)


class Balance(models.Model):
    # user id, 一个用户只能有一个余额
    user_id = models.PositiveIntegerField(unique=True)
    # 余额
    amount = models.PositiveIntegerField(default=0)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)


class ClockIn(models.Model):
    # user id, 一个用户可以有很多打卡
    user_id = models.PositiveIntegerField()
    # 打卡种类
    setup_id = models.PositiveIntegerField()
    # 图片 0
    image_0 = models.ImageField()
    # 打卡时间
    created_time = models.DateTimeField(auto_now_add=True)
