# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
import django.utils.timezone as timezone


def utcToLocal(utctime):
    import time
    from datetime import datetime
    return utctime + (datetime.fromtimestamp(time.time()) - datetime.utcfromtimestamp(time.time()))

class Users(models.Model):
    CLOTH_SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Middle'),
        ('L', 'Large'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    id = models.IntegerField(primary_key=True)                  # 数据库中的编号
    authority = models.IntegerField(default=0)                  # 权限 默认无权限为0，普通管理员为1，超管为2
    name = models.CharField(max_length=32, null=True)           # account9上的ID
    fullname = models.CharField(max_length=32, null=True)       # 姓名
    certification_type = models.IntegerField(default=0)         # 证件类型 默认0为身份证，护照为1
    certification_id = models.CharField(max_length=32, null=True)
                                                                # 证件号码
    mobile = models.CharField(max_length=32, null=True)         # 手机号
    classnumber = models.CharField(max_length=32, null=True)    # 班级
    email = models.CharField(max_length=32, null=True)          # 邮箱
    student_number = models.CharField(max_length=32, null=True) # 学号
    birthday = models.CharField(max_length=32, null=True)       # 生日
    room_address = models.CharField(max_length=32, null=True)   # 宿舍楼和房间号
    cloth_size = models.CharField(max_length=1, null=True, choices=CLOTH_SIZE_CHOICES)
                                                                # 衣服尺码
    gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES)
                                                                # 性别
    degree = models.IntegerField(null=True)                     # 攻读学位 0为本科 1为研究生

    # fullAddress = models.CharField(max_length=256, null=True)   # 详细地址
    # desc = models.TextField(default=u"暂无简介")                 # 个人简介
    # portrait = models.ImageField(null=True)                     # 头像
    # firstLogin = models.DateTimeField(default=timezone.now)     # 首次登录时间
    # lastLogin = models.DateTimeField(default=timezone.now)      # 上次登录时间

    def printAll(self):
        print u'<class HomePage.models.Users> {'
        print u'    ' + u'id = ' + unicode(self.id)
        print u'    ' + u'authority = ' + unicode(self.authority)
        print u'    ' + u'name = ' + unicode(self.name)
        print u'    ' + u'fullname = ' + unicode(self.fullname)
        print u'    ' + u'certification_type = ' + unicode(self.certification_type)
        print u'    ' + u'certification_id = ' + unicode(self.certification_id)
        print u'    ' + u'mobile = ' + unicode(self.mobile)
        print u'    ' + u'classnumber = ' + unicode(self.classnumber)
        print u'    ' + u'email = ' + unicode(self.email)
        print u'    ' + u'student_number = ' + unicode(self.student_number)
        print u'    ' + u'birthday = ' + unicode(self.birthday)
        print u'    ' + u'room_address = ' + unicode(self.room_address)
        print u'    ' + u'cloth_size = ' + unicode(self.cloth_size)
        print u'    ' + u'gender = ' + unicode(self.gender)
        print u'    ' + u'degree = ' + unicode(self.degree)
        print u'}'


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
        if now < self.timeRegSt:
            return 1
        elif now < self.timeRegEn:
            return 2
        elif now < self.timeEvnSt:
            return 3
        elif now < self.timeEvnEn:
            return 4
        else:
            return 4

    def printAll(self):
        print u'<class HomePage.models.Events> {'
        print u'    ' + u'id = ' + unicode(self.id)
        print u'    ' + u'name = ' + unicode(self.name)
        print u'    ' + u'desc = ' + unicode(self.desc)
        print u'    ' + u'timeRegSt = ' + unicode(self.timeRegSt)
        print u'    ' + u'timeRegEn = ' + unicode(self.timeRegEn)
        print u'    ' + u'timeEvnSt = ' + unicode(self.timeEvnSt)
        print u'    ' + u'timeEvnEn = ' + unicode(self.timeEvnEn)
        print u'    ' + u'maxRegCnt = ' + unicode(self.maxRegCnt)
        print u'    ' + u'nowRegCnt = ' + unicode(self.nowRegCnt)
        print u'    ' + u'teamMode = ' + unicode(self.teamMode)
        print u'    ' + u'teamMin = ' + unicode(self.teamMin)
        print u'    ' + u'teamMax = ' + unicode(self.teamMax)
        print u'    ' + u'getStatus() = ' + unicode(self.getStatus())
        print u'}'


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
    score = models.CharField(max_length=256, null=True)         # 成绩
    prize = models.CharField(max_length=256, default='0')         # 获奖情况

    def printAll(self):
        print u'<class HomePage.models.Signs> {'
        print u'    ' + u'eventId = ' + unicode(self.eventId)
        print u'    ' + u'userId = ' + unicode(self.userId)
        print u'    ' + u'teamSize = ' + unicode(self.teamSize)
        print u'    ' + u'teamMate = ' + unicode(self.teamMate)
        print u'    ' + u'timeReg = ' + unicode(self.timeReg)
        print u'    ' + u'exmTime = ' + unicode(self.exmTime)
        print u'    ' + u'exmStatus = ' + unicode(self.exmStatus)
        print u'    ' + u'score = ' + unicode(self.score)
        print u'    ' + u'prize = ' + unicode(self.prize)
        print u'}'

class IMG(models.Model):
    id = models.IntegerField(primary_key=True)                  # 数据库中的编号
    img = models.ImageField(upload_to='img')                    # 图片本身，本质上是图片文件在HomePage/static/media/下的相对路径
    name = models.CharField(max_length=20)                      # 一坨用来显示在首页上的文字
    detail = models.TextField(default='暂无')                    # 另一坨用来显示在首页上的文字
    imgtype = models.IntegerField(default=0)                    # 不知道这是什么

    def printAll(self):
        print u'<class HomePage.models.IMG> {'
        print u'    ' + u'id = ' + unicode(self.id)
        print u'    ' + u'img = ' + unicode(self.img)
        print u'    ' + u'name = ' + unicode(self.name)
        print u'    ' + u'detail = ' + unicode(self.detail)
        print u'    ' + u'imgtype = ' + unicode(self.imgtype)
        print u'}'
