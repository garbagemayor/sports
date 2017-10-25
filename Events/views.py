# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from HomePage.models import Events
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from HomePage.models import Sign

# Create your views here.
def index(request):
    print request.method
    events_list=list(Events.objects.all()[::-1])
    for l in events_list:
        l.s2 = gets2(l.status)
        l.s3 = gets3(l.status)
    paginator=Paginator(events_list, 3)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    
    return render(request, 'Events/events.html', {'events_list':events_list})

@csrf_exempt 
def page(request, Id):    
    events = Events.objects.get(id=Id)
    events.s2 = gets2(events.status)
    events.s3 = gets3(events.status)
    if request.method == "POST":
        s = Sign.objects.get_or_create(userid=request.session['userid'], eventsid=Id, status=1)
        if (s[1]):
            status=1
        else:
            status=2

        return render(request, 'Events/page.html', {'events':events, 'status':json.dumps(status)})
    else:
        return render(request, 'Events/page.html', {'events':events})


def gets2(i):
    if i == 1:
        return "即将开始"
    elif i == 2:
        return "正在报名"
    elif i == 3:
        return "报名已截止"
    elif i == 4:
        return "比赛已结束"
    else:
        return "???"

def gets3(i):
    if i == 1:
        return "info"
    elif i == 2:
        return "success"
    elif i == 3:
        return "danger"
    elif i == 4:
        return "warning"
