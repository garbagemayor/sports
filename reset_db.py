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

from Users.models import Notification, NotificationController
from HomePage.models import Users, Events, Signs, IMG, Broadcast, Team, ImgLabel
import django.utils.timezone as timezone
import datetime

print u'在Users表中添加对象'

'''
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
'''

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

print u'在Team表中添加对象'

i = 0
i += 1
Team.objects.get_or_create(id=i)
g = Team.objects.get(id=i)
g.sport = u'游泳'
g.name = u'计算机系游泳队'
g.achievement = u'贵系泳队在07年获得了马杯冠军，此后在当年的黄金一代全部毕业离校之后，开始走下坡路，团体排名稳定在五到八名之间，但在去年的马杯赛场上，贵系健儿们顶住压力，捷报频传，最终取得了甲组男团第三名的优异成绩。'
g.captain = u'吴雨舟'
g.athlete = u'谢晓晖'
g.detail = u' 贵系游泳队是一个温暖的大家庭，在这儿我们有和谐男女比，每次一小时的训练安排，轻松又愉快。我们在平时的训练中也会提供相关的技术指导，让你完成从入门到精通的飞跃。提高技术、瘦身塑形、享受生活，贵系泳队欢迎你！'
g.train = u'训练安排及内容:开学前六周，每周固定1~2次训练。比赛前四周，每周固定2~3次强度训练。'
g.joinus = u'加入我们:基本要求：能够踩水30秒\n能够连续游200米（不限泳姿）\n热爱游泳，积极参加训练\nPS:妹子我们当然是欢迎的啦，\n只要你愿意来，\n我们就在这里等你！'
g.headline = True
g.save()

i += 1
Team.objects.get_or_create(id=i)
g = Team.objects.get(id=i)
g.sport = u'男足'
g.name = u'计算机系男子足球队'
g.achievement = u'计算机系足球队是马杯上的传统强队，从2013年开始已经连续4年打入马杯甲组八强，并且在2014年获得马杯甲组季军。'
g.captain = u'丁豪'
g.athlete = u'刘加贺'
g.detail = u'球队球风稳健，敢于拼搏。球队今年进行大换血，在刘加贺，丁孝基等一批核心球员的毕业离队的同时，我们也迎来了21世纪第一个足球特长生，校队核心后防刘明辉。在这个新老交替的关键时刻，我们需要更多的新鲜血液加入，为计算机系足球队带来无限的可能，为球队的未来打下坚实的基础。'
g.train = u'训练安排及内容:每周一场热身赛（11人制，90分钟）\n每周一次基本功训练（周末晚，2个小时）\n不定期体能训练（周中晚，40分钟）\n新生基本功训练（针对大一新生，持续一年，一周4次，一次50分钟'
g.joinus = u'加入我们:一. 集体选拔：\n(1) 基本功测试（占分30分）1.足球踢远 2.15米短传    3.一次性巅球\n4.50米冲刺跑 5.6*20折返跑 6.30米长传\n(2) 系内组织选拔赛（占分70分）\n新人（或者新老）对抗，11人制，90分钟\n通过选拔赛表现进行选拔。时间地点待定'
g.headline = False
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/Picture2.png'
g.name = u'李晨曦'
g.detail = u'李晨曦，清华大学计算机系2013级博士生，马拉松国家二级运动员，曾创下北京国际马拉松赛全程2小时51分18秒完赛的个人最佳成绩，42.195千米的赛道，平均每千米用时约4分4秒，被称为“清华马拉松第一人”，原虎扑翻译团版主、虎扑新声编辑。'
g.headline = True
g.save()

print u'在IMG表中添加对象'

i = 0
i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/o_1bvhfaodp1a9d9a6csm1sq3iv19.jpg'
g.name = u'合照'
g.detail = u'泳队合照'
g.imgtype = 1
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_7516.JPG'
g.name = u'传奇'
g.detail = u'努力就能成功'
g.imgtype = 1
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_0128.jpg'
g.name = u'男足'
g.detail = u'合照'
g.imgtype = 2
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_0128.jpg'
g.name = u'球王'
g.detail = u'球王过人精彩瞬间'
g.imgtype = -1
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/IMG_0141.jpg'
g.name = u'姚指导'
g.detail = u'姚指导回眸一笑'
g.imgtype = -1
g.headline = True
g.save()

i += 1
IMG.objects.get_or_create(id=i)
g = IMG.objects.get(id=i)
g.url = u'http://oblc5mnxs.bkt.clouddn.com/o_1bvhjn2821e1gh528qs1a0j5qp9.jpg'
g.imgtype = -2
g.headline = True
g.save()

print u'在ImgLabel表中添加对象'

i = 0
i += 1
ImgLabel.objects.get_or_create(id=i)
g = ImgLabel.objects.get(id=i)
g.imgtype = -2
g.label = u'设为首页背景'
g.save()

i += 1
ImgLabel.objects.get_or_create(id=i)
g = ImgLabel.objects.get(id=i)
g.imgtype = -1
g.label = u'设为风采展示'
g.save()

i += 1
ImgLabel.objects.get_or_create(id=i)
g = ImgLabel.objects.get(id=i)
g.imgtype = -3
g.label = u'从主页撤回'
g.save()

i += 1
ImgLabel.objects.get_or_create(id=i)
g = ImgLabel.objects.get(id=i)
g.imgtype = -4
g.label = u'彻底删除'
g.save()

for team in Team.objects.all():
    i += 1
    ImgLabel.objects.get_or_create(id=i)
    g = ImgLabel.objects.get(id=i)
    g.imgtype = team.id
    g.label = team.name
    g.save()

print u'在Notification表中添加对象'

print u'添加完成'

del Users, Events, Signs, IMG, Broadcast
del timezone
del datetime
del django

if platform == "win32":
    Popen('pause', shell=True).wait()
