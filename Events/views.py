# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Signs as Sign
from HomePage.models import Events, Users
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.contrib import messages
import pyqrcode


# Create your views here.
def index(request):
    events_list = list(Events.objects.all()[::-1])
    for l in events_list:
        l.s2 = gets2(l.getStatus())
        l.s3 = gets3(l.getStatus())
    paginator=Paginator(events_list, 3)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    return render(request, 'Events/events.html', {'events_list': events_list})


@csrf_exempt
def page(request, Id):
    events = Events.objects.get(id=Id)
    events.status=events.getStatus()
    events.s2 = gets2(events.getStatus())
    events.s3 = gets3(events.getStatus())
    return render(request, 'Events/page.html', {'events':events})


def delete_events(request, Id):
    events = Events.objects.get(id=Id)
    if request.method == "GET":
        if request.session['userid']:
            if request.session['auth'] > 0:
                Events.objects.filter(id=Id).delete()
                Sign.objects.filter(eventsid=Id).delete()
                messages.add_message(request, messages.INFO, '删除成功！')
            else:
                messages.add_message(request, messages.INFO, '当前用户无此操作权限！')
        else:
            messages.add_message(request, messages.INFO, '请登录！')
            return HttpResponseRedirect('/authorized/')

        return HttpResponseRedirect('/events/')
    else:
        return HttpResponseRedirect('/events/')


def setprizes(request, Id):    
    events = Events.objects.get(id=Id)
    if request.method == "POST":
        print request.POST['rank_1']
        for i in range(1, 8):
            if not (request.POST['rank_'+str(i)] and request.POST['score_'+str(i)] and request.POST['number_'+str(i)]):
                messages.add_message(request, messages.INFO, '请完整填上全部信息！')
                return render(request, 'Events/setprizes.html', {'event':events, 'prize_number':range(1, 8)})
            
        for i in range(1, 8):
            u=Users.obejcts.filter(student_number=request.POST['number_'+i])
            if not u[0]:
                messages.add_message(request, messages.INFO, request.POST['number_'+i]+'不是有效学号！')
                return render(request, 'Events/setprizes.html', {'event':events, 'prize_number':range(1, 8)})
        for i in range(1, 8):
            u=Users.obejcts.filter(student_number=request.POST['number_'+i])
            u=u[0]
            Sign.objects.filter(userId=u.id, eventId=Id).update(score=request.POST['score_'+i], prize=i)
        return HttpResponseRedirect('/events/viewprizes/'+Id+'/')
                
        
    return render(request, 'Events/setprizes.html', {'event':events, 'prize_number':range(1, 8)})

def viewprizes(request, Id):
    events = Events.objects.get(id=Id)
    s=Sign.objects.filter(eventId=Id).exclude(prize='0')
    prize_list=[]
    for i in s:
        prize={}
        prize.rank=s.prize
        user=Users.objects.get(id=s.userId)
        prize.number=user.student_number
        prize.name=user.fullname
        prize.score=s.score
        prize_list.append(prize)
    return render(request, 'Events/prizes.html', {'event':events, 'prize_list':prize_list})

def nextphase(request, Id):
    events = Events.objects.get(id=Id)
    if request.method == "GET":
        if request.session['userid']:
            if request.session['auth'] > 0:
                e = Events.objects.get(id=Id)
                e.status += 1
                if e.status >= 5:
                    e.status = 1
                e.save()
                messages.add_message(request, messages.INFO, '修改成功！')
            else:
                messages.add_message(request, messages.INFO, '当前用户无此操作权限！')
        else:
            messages.add_message(request, messages.INFO, '请登录！')
            return HttpResponseRedirect('/authorized/')
        return HttpResponseRedirect('/events/' + Id)
    else:
        return HttpResponseRedirect('/events/' + Id)


def sign(request, Id):
    events = Events.objects.get(id=Id)
    if request.session['userid']:
        sf = Sign.objects.filter(userId=request.session['userid'], eventId=Id)
        if len(sf) >= 1:
            messages.add_message(request, messages.INFO, '请勿重复报名！')
        else:
            s = Sign.objects.create(userId=request.session['userid'], eventId=Id)
            s.teamSize = 1
            import django.utils.timezone as timezone
            s.timeReg = timezone.now()
            s.exmStatus = 1
            messages.add_message(request, messages.INFO, '报名成功！')
    else:
        messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect('/authorized/')

    return HttpResponseRedirect('/events/' + Id + '/');

def teamsign(request, Id):
    events = Events.objects.get(id=Id)
    if request.session['userid']:
        s = Sign.objects.get_or_create(userId=request.session['userid'], eventId=Id, exmStatus=1)
        if (s[1]):
            messages.add_message(request, messages.INFO, '报名成功！')
        else:
            messages.add_message(request, messages.INFO, '已报名！')
    else:
        messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect('/authorized/')

    return HttpResponseRedirect('/events/' + Id + '/');


def design(request, Id):
    events = Events.objects.get(id=Id)
    if request.session['userid']:
        sf = Sign.objects.filter(userId=request.session['userid'], eventId=Id)
        if len(sf) == 0:
            messages.add_message(request, messages.INFO, '您尚未报名！')
        else:
            if len(sf) >= 2:
                messages.add_message(request, messages.INFO, '您怎么这么强啊，居然在这一个比赛里面报次%d个名！您这么强，您爸妈知道吗？' % (len(sf)))
            for s in sf:
                if s.exmStatus == 1 or s.exmStatus == 3:
                    Sign.objects.filter(id=s.id).delete()
                    messages.add_message(request, messages.INFO, '取消成功！')
                elif s.exmStatus == 2:
                    messages.add_message(request, messages.INFO, '报名已审核通过，若要取消报名请联系管理员！')
    else:
        messages.add_message(request, messages.INFO, '请登录！')
        return HttpResponseRedirect('/authorized/')

    return HttpResponseRedirect('/events/' + Id + '/');


@csrf_exempt
def addevents(request):
    if request.method == "POST":
        if Events.objects.get_or_create(name=request.POST['name'], desc=request.POST['detail']):
            messages.add_message(request, messages.INFO, '成功添加赛事' + request.POST['name'] + '！')
            return HttpResponseRedirect('/events/')
    return render(request, "Events/addevents.html")


def gets2(i):
    if i == 1:
        return "即将开始"
    elif i == 2:
        return "正在报名"
    elif i == 3:
        return "报名已截止"
    elif i == 4:
        return "正在比赛"
    else:
        return "比赛已截止"


def gets3(i):
    if i == 1:
        return "info"
    elif i == 2:
        return "success"
    elif i == 3:
        return "danger"
    elif i == 4:
        return "warning"    
    else:
        return ""


def qrcode(request, Id):
    url = 'http://' + str(request.get_host()) + '/events/' + Id;
    print(url)
    code = pyqrcode.create(url)
    code.png('code.png', scale=8)
    image_data = open("code.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
