# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events, IMG, Users, Team
from HomePage.models import Broadcast
from HomePage.models import utcToLocal
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import django.utils.timezone as timezone

# Create your views here.

def index(request):
    team = Team.objects.get(headline=True,cate=1)
    team_img = list(IMG.objects.filter(headline=True,imgtype=Team.objects.get(headline=True,cate=1).id))
    celebrity = Team.objects.filter(headline=True,cate=2)[0]
    celebrity_img = list(IMG.objects.filter(headline=True,imgtype=celebrity.id))
    broadcast_list = list(Broadcast.objects.all()[::-1])
    game = list(IMG.objects.filter(headline=True,imgtype=-1))
    for b in broadcast_list:
        #print b.time.date()
        #print timezone.now().date()
        if b.time.date() >= timezone.now().date():
            b.new="新"
    game[0].active = 1
    game_len = range(len(game))
    background = IMG.objects.get(headline=True,imgtype=-2)
    events_list=Events.objects.all()[::-1]
    events1=[]
    events2=[]
    events3=[]
    for e in events_list:
        if e.getStatus()==1:
            events1.append(e)
        if e.getStatus()==2:
            events2.append(e)
        if e.getStatus()==5:
            events3.append(e)
    if len(events1)>5:
        events1=events1[:5]
    if len(events2)>5:
        events2=events2[:5]
    if len(events3)>5:
        events3=events3[:5]
    if len(broadcast_list)>5:
        broadcast_list=broadcast_list[:5]

    positive_energy_sentence = [
        u"从来不会轻易被打败 我们只会越来越强",
        u"只要你不回避与退缩 生命的掌声终会为你响起",
        u"认真你就输了 一直认真你就赢了",
        u"如果这世界上真有奇迹 那只是努力的另一个名字",
        u"世界上总会有人成功 为什么不能是你呢",
        u"任何人的成功 都不是虚头 他们一定付出了你没有想到的努力和代价",
        u"人不断地成长 就是为了超越环境的限制",
        u"没有过不去的阴雨天 也没有永远的晴天",
        u"人生没有容易的事情 如果有容易的事 人们不都去做了么",
        u"无论你现在到底有多艰难 请不要轻易放弃所坚持的东西",
        u"风雨中这是一场无火的战争 需要战胜的只有自己",
        u"成功者找方法 失败者找理由",
        # 都是这里挑选的： http://www.tcomall.com/post/1871.html
    ]
    # len_team = 0 if team == None else len(team)
    # for i in range(len_team):
    team.sentence = positive_energy_sentence[0 % len(positive_energy_sentence)]

    return render(request, "HomePage/newhomepage.html",
                  {'events1': events1,
                   'events1_len' : len(events1),
                   'events2': events2,
                   'events2_len' : len(events2),
                   'events3': events3,
                   'events3_len' : len(events3),
                   'team': team,
                   'team_img': team_img,
                   'celebrity': celebrity,
                   'celebrity_img': celebrity_img,
                   'game': game,
                   'background': background,
                   'broadcast':broadcast_list,
                   'game_len': game_len})

def broadcast(request):
    broadcast_list = list(Broadcast.objects.all()[::-1])
    for b in broadcast_list:
        #print b.time.date()
        if b.time.date() >= timezone.now().date():
            b.new="新"
    paginator = Paginator(broadcast_list, 10)
    page = request.GET.get('page')
    try:
        broadcast_list = paginator.page(page)
    except PageNotAnInteger:
        broadcast_list = paginator.page(1)
    except EmptyPage:
        broadcast_list = paginator.page(paginator.num_pages)

    return render(request, 'HomePage/broadcast.html', {'broadcast': broadcast_list})

def broadcastpage(request, Id):
    b = Broadcast.objects.filter(id=Id)
    if b:
        b=b[0]
        b.time = utcToLocal(b.time).strftime("%Y-%m-%d %H:%M:%S")
        if len(Users.objects.filter(id=b.publisher)) > 0:
            b.publishername = Users.objects.filter(id=b.publisher)[0].name
        else:
            b.publishername = "系统"
        return render(request, 'HomePage/broadcastpage.html', {'broadcast': b})
    else:
        return render(request, 'HomePage/broadcastpage.html')


def addbroadcast(request):    
    if request.method == "POST":
        if not request.POST['title']:
            messages.add_message(request, messages.INFO, "标题不能为空！")
            return render(request, "HomePage/addbroadcast.html")

        Broadcast.objects.create(title=request.POST['title'], detail=request.POST['detail'], publisher=request.session['userid'])
        messages.add_message(request, messages.INFO, "成功发布公告'"+request.POST['title']+"'！")
        return HttpResponseRedirect('/broadcast/')
    return render(request, "HomePage/addbroadcast.html")

def faq(request):

    return render(request, 'HomePage/faq.html')
