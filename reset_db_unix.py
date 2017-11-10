# -*- coding: utf-8 -*-

import os
import django
from subprocess import Popen

os.remove('db.sqlite3')
Popen('python2 manage.py makemigrations', shell=True).wait()
Popen('python2 manage.py migrate --run-syncdb', shell=True).wait()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SportsRegistration.settings")
django.setup()

from HomePage.models import Users, Events, Signs
import django.utils.timezone as timezone
import datetime

print u'在Users表中添加对象'

i = 0
i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'nodgd'
u.fullname = u'董又铭'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'tyt123'
u.fullname = u'谭懿峻'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'luoy15'
u.fullname = u'罗华一'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'yangjy15'
u.fullname = u'杨跻云'
u.authority = 2
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'userA'
u.fullname = u'用户A'
u.authority = 1
u.save()

i += 1
Users.objects.get_or_create(id=i)
u = Users.objects.get(id=i)
u.name = u'userB'
u.fullname = u'用户B'
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
e.name = u'正在报名的个人比赛'
e.timeRegSt = t1
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
e.name = u'正在报名的团队比赛，2~4人'
e.timeRegSt = t1
e.timeRegEn = t2
e.timeEvnSt = t2
e.timeEvnEn = t2
e.teamMode = 1
e.teamMin = 2
e.teamMax = 4
e.save()

print u'在IMG表中添加对象'

i = 0
i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.img = u'img/team.jpg'
g.name = u'计算机系女篮'
g.detail = u'2015年建队，队伍成员不仅有充满活力的本科生，还有球场经验老道的研究生学姐。虽然队史不长，但贵系女篮在马杯赛 事上敢打敢拼，已经成为了一支不容小觑的新生力量。'
g.imgtype = 0
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.img = u'img/celebrity.jpg'
g.name = u'李晨曦'
g.detail = u'李晨曦，清华大学计算机系2013级博士生，马拉松国家二级运动员，曾创下北京国际马拉松赛全程2小时51分18秒完赛的个人最佳成绩，42.195千米的赛道，平均每千米用时约4分4秒，被称为“清华马拉松第一人”，原虎扑翻译团版主、虎扑新声编辑。'
g.imgtype = 1
g.save()

print u'添加完成'

del Users, Events, Signs
del timezone
del datetime
del django
