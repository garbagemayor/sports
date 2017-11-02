# -*- coding: utf-8 -*-
from HomePage.models import Users, Events, Signs
import django.utils.timezone as timezone
import datetime

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

