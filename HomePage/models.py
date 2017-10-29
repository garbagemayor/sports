# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class Users(models.Model):
    id = models.IntegerField(primary_key=True)                  # 数据库中的编号
    account9Id = models.CharField(max_length=32, null=True)     # account9上的ID
    fullname = models.CharField(max_length=32, null=True)       # 姓名
    idid = models.CharField(max_length=32, null=True)           # 身份证号
    gender = models.CharField(max_length=4, null=True)          # 性别
    birthday = models.DateField(null=True)                      # 生日
    age = models.IntegerField(null=True)                        # 年龄
    cloSize = models.CharField(max_length=1, null=True)         # 衣服尺码
    mobile = models.CharField(max_length=32, null=True)         # 手机号
    email = models.CharField(max_length=64, null=True)          # 邮箱
    grade = models.CharField(max_length=32, null=True)          # 在读学位
    classNum = models.CharField(max_length=32, null=True)       # 班级
    stuID = models.CharField(max_length=32, null=True)          # 学号
    dormitory = models.CharField(max_length=32, null=True)      # 宿舍
    address = models.CharField(max_length=256, null=True)       # 详细地址
    desc = models.TextField(default=u"暂无简介")                 # 个人简介
    portrait = models.ImageField(null=True)                     # 头像
    firstLogin = models.DateTimeField(default=timezone.now)     # 首次登录时间
    lastLogin = models.DateTimeField(default=timezone.now)      # 上次登录时间
    online = models.BooleanField(default=True)                  # 当前是否在线
    authority = models.IntegerField(default=0)                  # 权限，默认无权限为0，普通管理员为1，超管为2


class Events(models.Model):
    id = models.IntegerField(primary_key=True)                  # 数据库中的编号
    name = models.CharField(default="", max_length=256)         # 赛事名称，例如“2017校园马拉松”
    desc = models.TextField(default=u"暂无简介")                 # 赛事简介，例如“暂无简介”
    timeRegSt = models.DateTimeField(default=timezone.now)      # 报名开始时间
    timeRegEn = models.DateTimeField(default=timezone.now)      # 报名截止时间
    timeEvnSt = models.DateTimeField(default=timezone.now)      # 比赛开始时间
    timeEvnEn = models.DateTimeField(default=timezone.now)      # 比赛截止时间
    maxRegCnt = models.IntegerField(default=-1)                 # 最大报名人数/队伍数，-1表示无限制
    nowRegCnt = models.IntegerField(default=0)                  # 已报名人数/队伍数
    teamMode = models.IntegerField(default=0)                   # 0个人比赛，1团队比赛
    teamMin = models.IntegerField(null=True)                    # 团队比赛的最低人数
    teamMax = models.IntegerField(null=True)                    # 团队比赛的最多人数
    # 对报名选手的要求（算了别写了，统统交给管理员审核吧）
    # reqSex = models.CharField(default="", max_length=4)         # 限制性别
    # reqDpt = models.CharField(default="", max_length=256)       # 限制院系
    # reqGrd = models.CharField(default="", max_length=256)       # 限制年级

    def getStatus(self):
        now = timezone.now()
        if now < self.timeTegSt:
            return 1
        elif now < self.timeRegEn:
            return 2
        elif now < self.timeEvnSt:
            return 3
        elif now < self.timeEvnEn:
            return 4
        else:
            return 5



class Signs(models.Model):
    id = models.IntegerField(primary_key=True)                  # 数据库中的编号
    eventId = models.IntegerField(null=True)                    # 赛事的数据库编号
    userId = models.IntegerField(null=True)                     # 用户的数据库编号，是队长
    teamSize = models.IntegerField(default=1)                   # 个人报名就是1，团队报名时是队伍的人数
    teamMate = models.CharField(validators=[validate_comma_separated_integer_list], max_length=256, null=True)
                                                                # 队友的用户数据库编号列表，包含userId，至多256人一起报名
    timeReg = models.DateTimeField(default=timezone.now)        # 报名时间
    exmTime = models.DateTimeField(null=True)                   # 审核时间
    exmStatus = models.IntegerField(default=1)                  # 1等待审核，2审核通过报名成功，3审核GG报名无效
    prize = models.CharField(max_length=256, null=True)         # 获奖情况

