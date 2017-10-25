# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
import json
from HomePage.models import User, Sign, Events
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
    request.session['userid']=user[0].id
    request.session['auth']=user[0].authority
    return HttpResponseRedirect("/events/")

def logout(request):
    if (request.session['username']):
        del request.session['username']
        del request.session['userid']        
        del request.session['auth']
    return HttpResponseRedirect("/")

def my_information(request):
    return render(request, "Users/users.html")

def my_events(request):
    if (request.session['userid']):
        render(request, "Users/users.html")
        events_list = []
        elist = Sign.objects.filter(userid=request.session['userid'])
        for e in elist:
            tmp = Events.objects.get(id=e.eventsid)
            tmp.s2 = gets2(tmp.status)
            events_list.append(tmp)
        paginator=Paginator(events_list, 3)
        page = request.GET.get('page')
        try:
            events_list = paginator.page(page)
        except PageNotAnInteger:
            events_list = paginator.page(1)
        except EmptyPage:
            events_list = paginator.page(paginator.num_pages)
        
            
        return render(request, 'Events/myevents.html', {'events_list':events_list})
    else:
        HttpResponseRedirect("/authorized/")





def send_email(request):
    email_title = 'title'
    email_body = 'content'
    EMAIL_FROM = '924486024@qq.com'
    email = 'luohy15@mails.tsinghua.edu.cn'
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        return HttpResponseRedirect('/')

def gets2(i):
    if i == 1:
        return "info"
    elif i == 2:
        return "success"
    elif i == 3:
        return "danger"
    elif i == 4:
        return "warning"
