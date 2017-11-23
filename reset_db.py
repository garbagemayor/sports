# -*- coding: utf-8 -*-

import os
import django
from subprocess import Popen
from sys import platform

try:
	os.remove('db.sqlite3')
except:
	''
if platform == "linux" or platform == "linux2":
    # linux
    Popen('python2 manage.py makemigrations', shell=True).wait()
    Popen('python2 manage.py migrate --run-syncdb', shell=True).wait()
elif platform == "darwin":
    # OS X
    Popen('python2 manage.py makemigrations', shell=True).wait()
    Popen('python2 manage.py migrate --run-syncdb', shell=True).wait()
elif platform == "win32":
    # Windows...
    Popen('py -2 manage.py makemigrations', shell=True).wait()
    Popen('py -2 manage.py migrate --run-syncdb', shell=True).wait()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SportsRegistration.settings")
django.setup()

from HomePage.models import Users, Events, Signs, IMG, Broadcast
import django.utils.timezone as timezone
import datetime

print u'在Users表中添加对象'

i = 0
i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'nodgd'
u.fullname = u'董又铭'
u.email = u'dongym15@mails.tsinghua.edu.cn'
u.student_number = u'2015011294'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'tyt123'
u.fullname = u'谭懿峻'
u.student_number = u'2015011292'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'luoy15'
u.fullname = u'罗华一'
u.email = u'luohy15@mails.tsinghua.edu.cn'
u.student_number = u'2015011305'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'yangjy15'
u.fullname = u'杨跻云'
u.student_number = u'2015011298'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'userA'
u.fullname = u'用户A'
u.student_number = u'123'
u.authority = 1
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'userB'
u.fullname = u'用户B'
u.student_number = u'233'
u.authority = 1
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'userC'
u.fullname = u'用户C'
u.authority = 0
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'userD'
u.fullname = u'用户D'
u.authority = 0
u.save()

print u'在Events表中添加对象'

t0 = timezone.now()
t1 = t0 + datetime.timedelta(days=-1000)
t2 = t0 + datetime.timedelta(days=1000)

i = 0
i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'等待报名的个人比赛'
e.timeRegSt = t2
e.timeRegEn = t2
e.timeEvnSt = t2
e.timeEvnEn = t2
e.teamMode = 0
e.save()

i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'报名截止的个人比赛'
e.timeRegSt = t1
e.timeRegEn = t1
e.timeEvnSt = t2
e.timeEvnEn = t2
e.teamMode = 0
e.save()

i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'正在进行的个人比赛'
e.timeRegSt = t1
e.timeRegEn = t1
e.timeEvnSt = t1
e.timeEvnEn = t2
e.teamMode = 0
e.save()

i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'已经结束的个人比赛'
e.timeRegSt = t1
e.timeRegEn = t1
e.timeEvnSt = t1
e.timeEvnEn = t1
e.teamMode = 0
e.save()

i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'正在报名的个人比赛(1)'
e.timeRegSt = t1
e.timeRegEn = t2
e.timeEvnSt = t2
e.timeEvnEn = t2
e.teamMode = 0
e.maxRegCnt = 30
e.save()

i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'正在报名的个人比赛(2)'
e.timeRegSt = t1
e.timeRegEn = t2
e.timeEvnSt = t2
e.timeEvnEn = t2
e.teamMode = 0
e.maxRegCnt = 1
e.save()

i += 1
Events.objects.get_or_create(id=i)
e = Events.objects.get(id=i)
e.name = u'正在报名的团队比赛，2~4人'
e.timeRegSt = t1
e.timeRegEn = t2
e.timeEvnSt = t2
e.timeEvnEn = t2
e.teamMode = 1
e.teamMin = 2
e.teamMax = 4
e.maxRegCnt = 5
e.save()

print u'在Broadcast表中添加信息'

Broadcast.objects.get_or_create(id=1)
b = Broadcast.objects.get(id=1)
b.title = u'冬季迷你马拉松来啦!!!'
b.detail = u'什么都没有'
b.publisher = 2
b.save()

Broadcast.objects.get_or_create(id=2)
b = Broadcast.objects.get(id=2)
b.title = u'听说这样可以算阿甘?'
b.detail = u'哈哈哈'
b.publisher = 2
b.save()

Broadcast.objects.get_or_create(id=3)
b = Broadcast.objects.get(id=3)
b.title = u'呃呃鹅鹅鹅鹅鹅鹅'
b.detail = u'什么都没有'
b.publisher = 2
b.save()

print u'在IMG表中添加对象'

i = 0
i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_0068.JPG'
g.name = u'新的风暴已经出现'
g.detail = u'贵系毽绳队夺得马杯甲组总分第一!'
g.imgtype = 0
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_0128.jpg'
g.name = u'球王'
g.detail = u'球王过人精彩瞬间'
g.imgtype = 1
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_0141.jpg'
g.name = u'姚指导'
g.detail = u'姚指导回眸一笑'
g.imgtype = 1
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/Picture2.png'
g.name = u'李晨曦'
g.detail = u'李晨曦，清华大学计算机系2013级博士生，马拉松国家二级运动员，曾创下北京国际马拉松赛全程2小时51分18秒完赛的个人最佳成绩，42.195千米的赛道，平均每千米用时约4分4秒，被称为“清华马拉松第一人”，原虎扑翻译团版主、虎扑新声编辑。'
g.imgtype = 2
g.headline = True
g.save()

print u'添加完成'

del Users, Events, Signs, IMG, Broadcast
del timezone
del datetime
del django

if platform == "win32":
    Popen('pause', shell=True).wait()
