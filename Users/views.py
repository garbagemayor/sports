# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import json
from django.core.mail import send_mail
from HomePage.models import Sign
from HomePage.models import Events
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def auth(request):
    r = requests.post('https://accounts.net9.org/api/access_token?client_id=0eHhovG3K1NYkhbnYuYmej1h9wY&client_secret=moK3EkYsQvossfoMwmCd&code='
            + request.GET['code'])
    rr = requests.get('https://accounts.net9.org/api/userinfo?access_token=' + r.json()['access_token'])
    j=rr.json()
    user=User.objects.get_or_create(name=j['user']['name'], email=j['user']['email'], mobile=j['user']['mobile'], fullname=j['user']['fullname'], classnumber=j['user']['groups'][0])
    request.session['username']=j['user']['name']
    request.session['userid']=user[0].id;
    return HttpResponseRedirect("/events/")

def logout(request):
    if (request.session['username']):
        del request.session['username']
    return HttpResponseRedirect("/")

def send_email(request):
    email_title = 'title'
    email_body = 'content'
    EMAIL_FROM = '924486024@qq.com'
    email = 'luohy15@mails.tsinghua.edu.cn'
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    if send_status:
        return HttpResponseRedirect('/')

def my_events(request):
    # TODO: my_events_list=list(Events.objects.get(userid=""))
    sign_list=list(Sign.objects.get(userid="7"))
    events_list = []
    for event in sign_list:
        l = list(Events.objects.get(id=event.eventsid))
        if l.status =="success":
            l.event_status = "正在报名"
        elif l.status =="error":
            l.event_status = "已截止"
        elif l.status =="info":
            l.event_status = "尚未开始"
        events_list.add(l)
    paginator=Paginator(events_list, 3)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)
    return render(request, 'Users/my_events.html', {'events_list':events_list,
        'sign_list':sign_list})

def my_event(request, Id):
    events=Events.objects.get(id=Id)
    return render(request, 'Events/page.html', {'events':events})
>>>>>>> dev
